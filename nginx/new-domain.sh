#!/bin/sh

set -e

DOMAIN=$1
DOCKER_NAME=$2
DOCKER_PORT=$3

cat <<EOF > "/tmp/$DOCKER_NAME.ssl.cfg"
[ req ]
req_extensions     = req_ext
distinguished_name = req_distinguished_name
prompt             = no

[req_distinguished_name]
commonName=$DOMAIN

[req_ext]
subjectAltName   = @alt_names

[alt_names]
DNS.1  = $DOMAIN
DNS.2  = www.$DOMAIN
EOF
openssl req -x509 -config "/tmp/$DOCKER_NAME.ssl.cfg"  -extensions req_ext -nodes -days 90 -newkey rsa:2048 -sha256 -keyout "/letsencrypt/certificates/www.$DOMAIN.key" -out "/letsencrypt/certificates/www.$DOMAIN.crt"
rm "/tmp/$DOCKER_NAME.ssl.cfg"
echo 'Done'

# For debugging problems you could uncomment the echo commands below.
mkdir -p "/webroot/www.$DOMAIN/.well-known/acme-challenge"
# echo "www.$DOMAIN -> $DOCKER_NAME:$DOCKER_PORT webroot" > "/webroot/www.$DOMAIN/.well-known/acme-challenge/hello"
mkdir -p "/media/www.$DOMAIN/"
# echo "www.$DOMAIN -> $DOCKER_NAME:$DOCKER_PORT media" > "/media/www.$DOMAIN/hello"
mkdir -p "/static/www.$DOMAIN/"
# echo "www.$DOMAIN -> $DOCKER_NAME:$DOCKER_PORT static" > "/static/www.$DOMAIN/hello"

cat << EOF > "/etc/nginx/conf.d/docker/$DOCKER_NAME.conf"
upstream $DOCKER_NAME {
  server $DOCKER_NAME:$DOCKER_PORT;
}

server {
  listen 80;
  server_name www.$DOMAIN $DOMAIN;

  location /.well-known/acme-challenge/ {
    root /webroot/www.$DOMAIN/;
  }

  location / {
    return 301 https://\$host\$request_uri;
  }
}

server {
  listen 443 ssl;
  server_name www.$DOMAIN;
  ssl_certificate /letsencrypt/certificates/www.$DOMAIN.crt;
  ssl_certificate_key /letsencrypt/certificates/www.$DOMAIN.key;

  # ssl_session_cache builtin:1000 shared:SSL:10m;
  # ssl_protocols TLSv1 TLSv1.1 TLSv1.2;
  # ssl_ciphers HIGH:!aNULL:!eNULL:!EXPORT:!CAMELLIA:!DES:!MD5:!PSK:!RC4;
  # ssl_prefer_server_ciphers on;
  # These are redirected to stdout by the Dockerfile
  access_log /var/log/nginx/access.log;
  error_log /var/log/nginx/error.log;
  location / {
    # client_max_body_size 20M;
    # To add basic authentication to v2 use auth_basic setting.
    # auth_basic "Registry realm";
    # auth_basic_user_file /etc/nginx/conf.d/www.$DOMAIN.htpasswd;
    proxy_set_header Host \$host;
    proxy_set_header X-Real-IP \$remote_addr;
    proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
    proxy_set_header X-Forwarded-Proto \$scheme;
    # Fix the "It appears that your reverse proxy set up is broken" error.
    proxy_pass http://web;
    proxy_read_timeout 90;
    proxy_redirect http://web https://www.$DOMAIN;
  }

  location /media/ {
    alias /media/web/;
  }

  location /static/ {
    alias /static/web/;
  }
}

EOF

echo 'Testing new configuration ...'
nginx -t
echo 'OK'
echo 'done.'
echo "Reloading Nginx with the self-signed certificates for www.$DOAMIN ..."
nginx -s reload
echo 'done'

# Add this to the lego commands for testing with the staging server:
# --server=https://acme-staging-v02.api.letsencrypt.org/directory
echo 'Attempting to get live certificates ...'
lego --accept-tos -m "$LETS_ENCRYPT_EMAIL" --http --http.webroot "/webroot/www.$DOMAIN" -d "www.$DOMAIN" -d "$DOMAIN" --path /letsencrypt run
echo 'done'

echo "Reloading Nginx with the live certificates for www.$DOAMIN ..."
nginx -s reload
echo 'done'

echo 'Adding the renew task to the daily cronjob ...'
cat << EOF >> "/etc/periodic/daily/www.$DOMAIN"
#!/bin/sh

set -e

echo "Cron running for www.$DOMAIN ... Sleeping ..."
sleep `tr -cd "[:digit:]" < /dev/urandom | head -c 4 # 9,999 seconds - roughly 2 hours 45m `
echo "Awake for  www.$DOMAIN ... Renewing ..."
lego --email="$LETS_ENCRYPT_EMAIL" --domains="www.$DOMAIN" --domains "$DOMAIN" --http --http.webroot "/webroot/www.$DOMAIN" --path /letsencrypt renew --days 30 --renew-hook="nginx -s reload"
echo "All done."
EOF
echo 'done.'

echo 'Checking cron ...'
run-parts --test /etc/periodic/daily
echo 'done'

echo 'Finished'


