FROM alpine:3.10 as base

RUN apk --no-cache add py-pip groff
RUN pip install --upgrade pip
RUN pip install awscli
RUN mkdir /root/.aws

FROM base as run
ENTRYPOINT ["/usr/bin/aws"]

# COPY get-metadata /usr/local/bin/get-metadata
