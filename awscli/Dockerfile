FROM alpine:3.11 as base

RUN apk --no-cache add python3 groff
RUN pip3 install --upgrade pip
RUN pip3 install awscli
RUN mkdir /root/.aws

FROM base as run
ENTRYPOINT ["/usr/bin/aws"]

# COPY get-metadata /usr/local/bin/get-metadata
