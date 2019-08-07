'''
Make some changes to your `docker-compose.yml`...

Use `mdillon/postgis:11-alpine` as the `image` in the `db` section of your `docker-compose.yml`, and change the local db volume mount from `- ./db:/var/lib/postgresql/data` to `- ./db.postgis:/var/lib/postgresql/data` if you already have one you want to keep:

```
  db:
    image: mdillon/postgis:11-alpine
    # image: postgres:alpine
    ports:
      - "5432:5432"
    volumes:
      - ./db.postgis:/var/lib/postgresql/data
```

Use `postgis://` as the engine in your `DATABASE_URL` in the `web` section.

```
  web:
    build: ./web
    volumes:
      - ./web:/code:rw
    ports:
      - "8000:8000"
    environment:
      PORT: 8000
      DJANGO_SETTINGS_MODULE: geod.settings.dev
      DATABASE_URL: postgis://postgres@db/postgres
      # DATABASE_URL: postgres://postgres@db/postgres
      MEDIA_AWS_ACCESS_KEY_ID: XXX
    ...
```

Edit the `web/Dockerfile` so the top two sections look like this:

```
FROM alpine:edge as runbase
RUN echo "http://dl-cdn.alpinelinux.org/alpine/edge/testing" > /etc/apk/repositories && echo "http://dl-cdn.alpinelinux.org/alpine/edge/community" >> /etc/apk/repositories && echo "http://dl-cdn.alpinelinux.org/alpine/edge/main" >> /etc/apk/repositories
RUN apk update
RUN apk add --update python3 postgresql-client libpq jpeg zlib libffi gdal geos proj proj-datumgrid geoip
RUN ln -s /usr/lib/libproj.so.15.1.0 /usr/lib/libproj.so
RUN pip3 install --upgrade pip

FROM runbase as buildbase
RUN echo "http://dl-cdn.alpinelinux.org/alpine/edge/testing" > /etc/apk/repositories && echo "http://dl-cdn.alpinelinux.org/alpine/edge/community" >> /etc/apk/repositories && echo "http://dl-cdn.alpinelinux.org/alpine/edge/main" >> /etc/apk/repositories
RUN apk update
RUN apk add --update build-base postgresql-dev libffi-dev zlib-dev jpeg-dev python3-dev gdal-dev geos-dev proj-dev geoip-dev
```

Now make sure the code in the bottom of this file is integrated into your settings.

For example, if you name this file `base_07_geo.py` you would want to change `dev.py` and `production_01_bucket.py` to import it like this:

```
from .base_07_geo import *
```

Then make sure this file imports this at the top to continue the chain:

```
from .base_06_timezone import *
```

You should now be able to run every step in the GeoDjango tutorial here:

    https://docs.djangoproject.com/en/2.2/ref/contrib/gis/

Bear in mind that if you ran `docker-compose up` before making these changes, you'll need to run migrations again because you now have a new database and different tables:

```
alias manage.py='docker-compose -f `pwd`/docker-compose.yml run --rm web python3 manage.py'
manage.py migrate
```

'''

for app in [
    'django.contrib.admin',
    'django.contrib.gis',
]:
    if app not in INSTALLED_APPS:
        INSTALLED_APPS.append(app)
