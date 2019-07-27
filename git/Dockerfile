FROM alpine:3.10 as base

RUN apk --no-cache add git openssh

FROM base as run
WORKDIR /repo
ENTRYPOINT ["git"]
