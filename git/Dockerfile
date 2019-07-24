FROM alpine:3.10 as base

RUN apk --no-cache add git

FROM base as run
ENTRYPOINT ["git"]
