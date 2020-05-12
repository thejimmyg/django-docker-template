FROM alpine:3.11 as base
RUN apk add --no-cache nginx lego tini

FROM base as run
RUN apk add --no-cache openssl apache2-utils

FROM run as run1
RUN apk add --no-cache su-exec

FROM run1 as run2
RUN apk --no-cache add shadow

FROM run2 as run3
RUN mkdir /run/nginx
RUN ln -sf /dev/stdout /var/log/nginx/access.log && ln -sf /dev/stderr /var/log/nginx/error.log
COPY ./bin/ /bin/
RUN chmod +x /bin/start-domain /bin/deploy-domain /bin/start-cron-and-nginx

EXPOSE 80
EXPOSE 443
ENTRYPOINT ["/sbin/tini", "-g", "--"]
CMD ["/bin/sh", "/bin/start-cron-and-nginx"]
