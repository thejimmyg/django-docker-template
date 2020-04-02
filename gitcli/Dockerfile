FROM alpine:3.11 as base

RUN apk --no-cache add git git-perl openssh

FROM base as run
WORKDIR /repo
ENTRYPOINT ["git"]
