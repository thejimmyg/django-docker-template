FROM alpine:3.11 as base
RUN apk add --no-cache nginx lego tini

FROM base as openssh
RUN apk add --no-cache openssl

FROM openssh as run
# Check the config options don't have unicode characters
# https://github.com/certbot/certbot/issues/5657
RUN grep -r -P '[^\x00-\x7f]' /etc/nginx || echo 'OK'
RUN mkdir /run/nginx
RUN ln -sf /dev/stdout /var/log/nginx/access.log && ln -sf /dev/stderr /var/log/nginx/error.log
COPY start-cron-and-nginx.sh /bin/start-cron-and-nginx
RUN chmod +x /bin/start-cron-and-nginx
COPY new-domain.sh /bin/new-domain
RUN chmod +x /bin/new-domain
# COPY cron /etc/cron.d/certbot
# COPY nginx.conf /etc/nginx/nginx.conf

EXPOSE 80
EXPOSE 443
ENTRYPOINT ["/sbin/tini", "-g", "--"]
CMD ["/bin/sh", "/bin/start-cron-and-nginx"]
