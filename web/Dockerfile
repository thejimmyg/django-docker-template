FROM python:3.7-alpine as runbase
RUN apk update
RUN apk add --update postgresql-client libpq jpeg zlib libffi
RUN pip3 install --upgrade pip

FROM runbase as buildbase
RUN apk update
RUN apk add --update build-base postgresql-dev libffi-dev zlib-dev jpeg-dev

FROM buildbase as pipdownload
ENV PYTHONUNBUFFERED 1
COPY ./requirements.txt /code/requirements.txt
RUN pip3 download -r /code/requirements.txt

FROM pipdownload as pip
RUN pip3 install -r /code/requirements.txt

FROM runbase as django
COPY --from=pip /usr/local/lib/python3.7/ /usr/local/lib/python3.7/
COPY --from=pip /usr/local/bin/ /usr/local/bin/
ENV PYTHONUNBUFFERED 1
RUN adduser -D -u 1000 django

FROM django as emptydjango
USER django
WORKDIR /code/
COPY . /code/
EXPOSE 8000
CMD ["/bin/sh", "/code/run.sh"]
