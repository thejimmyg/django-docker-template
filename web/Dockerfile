# syntax=docker/dockerfile:experimental

# For efficiency, using the same base image as # https://github.com/postgis/docker-postgis/blob/master/12-3.0/alpine/Dockerfile
# Which uses https://github.com/docker-library/postgres/blob/33bccfcaddd0679f55ee1028c012d26cd196537d/12/alpine/Dockerfile

FROM alpine:3.11 as runbase
RUN apk update
RUN apk add --no-cache python3 postgresql-client libpq jpeg zlib libffi
# Start geo
# RUN apk add --no-cache gdal geos proj proj-datumgrid geoip
# RUN ln -s /usr/lib/libproj.so.15.1.0 /usr/lib/libproj.so
# End geo

FROM runbase as buildbase
RUN apk update
RUN apk add --no-cache build-base postgresql-dev libffi-dev zlib-dev jpeg-dev python3-dev
# Start geo
# RUN apk add --no-cache gdal-dev geos-dev proj-dev geoip-dev
# End geo

# If you are using an old version of Docker don't use this section:
FROM buildbase as pipbaseinstall
COPY ./base-requirements.txt /code/base-requirements.txt
RUN --mount=type=cache,target=/root/.cache/pip pip3 install -r /code/base-requirements.txt && find /usr/lib/python3.8/ -name '*.pyc' | xargs rm -f

FROM pipbaseinstall as piplocal
COPY ./requirements.txt /code/requirements.txt
RUN --mount=type=cache,target=/root/.cache/pip pip3 install -r /code/requirements.txt && find /usr/lib/python3.8/ -name '*.pyc' | xargs rm -f
# Uncomment and use this instead:
#  FROM buildbase as pipbasedownload
#  ENV PYTHONUNBUFFERED 1
#  COPY ./base-requirements.txt /code/base-requirements.txt
#  # RUN pip3 install --upgrade pip
#  RUN pip3 download -r /code/base-requirements.txt
# 
#  FROM pipbasedownload as pipbaseinstall
#  # RUN pip3 install --upgrade pip
#  RUN pip3 install -r /code/base-requirements.txt && find /usr/lib/python3.8/ -name '*.pyc' | xargs rm -f
# 
#  FROM pipbaseinstall as pipreqdownload
#  ENV PYTHONUNBUFFERED 1
#  COPY ./requirements.txt /code/requirements.txt
#  # RUN pip3 install --upgrade pip
#  RUN pip3 download -r /code/requirements.txt
# 
#  FROM pipreqdownload as pipreqinstall
#  COPY ./requirements.txt /code/requirements.txt
#  # RUN pip3 install --upgrade pip
#  RUN pip3 install -r /code/requirements.txt && find /usr/lib/python3.8/ -name '*.pyc' | xargs rm -f
#  # Optionally you can install exactly the dependencies that were frozen
#  # in freeze.txt on first run of the web container but by default we
#  # let the specified requirements choose their own dependencies.
#  # RUN pip3 install -r /code/freeze.txt && find /usr/lib/python3.8/ -name '*.pyc' | xargs rm -f

FROM runbase as django
COPY --from=piplocal /usr/lib/python3.8/ /usr/lib/python3.8/
COPY --from=piplocal /usr/bin/ /usr/bin/
ENV PYTHONUNBUFFERED 1
RUN adduser -D -u 1000 django

FROM django as emptydjango
USER django
WORKDIR /code/
COPY . /code/
EXPOSE 8000
CMD ["/bin/sh", "/code/run.sh"]
