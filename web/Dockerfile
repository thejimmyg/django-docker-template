FROM alpine:3.10 as runbase
RUN apk update
RUN apk add --update python3 postgresql-client libpq jpeg zlib libffi
RUN pip3 install --upgrade pip

FROM runbase as buildbase
RUN apk update
RUN apk add --update build-base postgresql-dev libffi-dev zlib-dev jpeg-dev python3-dev

FROM buildbase as pipdownload
ENV PYTHONUNBUFFERED 1
COPY ./base-requirements.txt /code/base-requirements.txt
RUN pip3 download -r /code/base-requirements.txt

FROM pipdownload as pip
RUN pip3 install -r /code/base-requirements.txt

FROM pip as piplocal
COPY ./requirements.txt /code/requirements.txt
RUN pip3 install -r /code/requirements.txt

FROM runbase as django
COPY --from=piplocal /usr/lib/python3.7/ /usr/lib/python3.7/
COPY --from=piplocal /usr/bin/ /usr/bin/
ENV PYTHONUNBUFFERED 1
RUN adduser -D -u 1000 django

FROM django as emptydjango
USER django
WORKDIR /code/
COPY . /code/
EXPOSE 8000
CMD ["/bin/sh", "/code/run.sh"]
