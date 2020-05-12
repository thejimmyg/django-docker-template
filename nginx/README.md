## Setting up domains

First build and start the Nginx container (and containers that serve domains you want to test)

```
docker-compose up -d --build && docker-compose logs -f nginx web
```

Then connect to the running instance replacing `docker` with the name of the directory containing the `docker-compose.yml` file, or looking it up in the output of `docker ps`:

```
docker exec -it mysite_nginx_1 sh
```

From here you can use the `/bin/start-domain` script to create your Nginx config as well as a self-signed certificate to get you started for testing.
The script takes these arguments:

* `DOCKER_NAME` - a name for the configuration. This is usually the hostname Docker gives to the conatiner you intend to proxy to, but if you don't intend to use another container, just name it something sensible and unique.
* `MODE` - can be `www` or `bare`
* `DOMAIN` - the domain you want to host (without the `www` if you are using `MODE=www`
* `TEMPLATE` - can be `static`, `static-fallback`, `post` or `proxy`
* `DOCKER_PORT` - defaults to 80, and is only needed when using `post` or `proxy` templates

When `MODE` is `www` it sets up two hosts and redirects the bare domain to the HTTPS hosting of the `www.` subdomain, as well as creating a certificate for that handles both the bare domain and the `www` subdomain.

Here's an example:

First run:

```
start-domain some.example.com some bare post
```

There isn't any checking on the arguments, so be careful what you type.

Once this is run you'll see `conf.d/docker/some.conf` has been created on the host with the user and group ID specified in the `LETS_ENCRYPT_USER` environment variable in the `docker-compose.yml` file (so you usually set this to be the user you normally use on the host).

Once you accept the self-signed certificate or ignore security warnigns you'll see some the default for the template you set up.

You can edit the `conf.d/docker/some.conf` file to customise your config then test the changes by reloading Nginx in the same shell you ran `/bin/start-domain` in for the running Nginx container:

```
nginx -s reload
```

Repeat this process until you are happy that Nginx is configured correctly for all your domains, apart from the fact they are using self-signed certificates.

Of course, don't change the configuration at the top involving `.well-known` as this is needed for obtaining and renewing certificates.

If you need to create password files for basic auth you can use the `htpasswd` utility from the same shell.

e.g.:

```
htpasswd -c /etc/nginx/conf.d/docker/some.htpasswd some
```

No you are ready to get the offical certificates.

* Make sure `LETS_ENCRYPT_EMAIL` is set to the real email address of a
  person who has agreed to the terms and conditions of Let's Encrypt. Restart the container and shell if you've made a change.

  ```
  nginx:
    ...
    environment:
      LETS_ENCRYPT_EMAIL: "james@example.com"
  ```

* Make sure your live domains point to the Nginx container
* Run the `/bin/deploy-domain` script to run through the Lets Encrypt validation and set up the cron job. The commands use the same arguments as the first three arguments to `start-domain` and have to be given the same values.

You'll see from the output if there are any problems, if you are successful, your new certificates will be automatically served from your domains.

Everything that is needed to be able to restore the state of the container can be found in this `nginx` directory on the host, so this is all you need to back up. 

Type `exit` to exit from the shell when you are finished.


# Cleanup

```
rm -f nginx/conf.d/docker/*.conf nginx/conf.d/docker/*.htpasswd nginx/letsencrypt/certificates/*.crt nginx/letsencrypt/certificates/*.key
```
