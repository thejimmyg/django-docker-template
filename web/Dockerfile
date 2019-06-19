# # Use an official Python runtime as a parent image
# FROM python:3.7 as base
# LABEL maintainer="hello@django.io"
# # Set environment varibles
# ENV PYTHONUNBUFFERED 1
# ENV DJANGO_ENV dev
# 
# COPY ./requirements.txt /code/requirements.txt
# RUN pip install --upgrade pip
# # Install any needed packages specified in requirements.txt
# RUN pip install -r /code/requirements.txt
# RUN pip install gunicorn
# 
# from base as django
# # Copy the current directory contents into the container at /code/
# COPY . /code/
# # Set the working directory to /code/
# WORKDIR /code/
# EXPOSE 8000

FROM python:3.7-alpine as runbase
RUN apk update
RUN apk add --update postgresql-client libpq jpeg zlib libffi
RUN pip3 install --upgrade pip

FROM runbase as buildbase
RUN apk update
RUN apk add --update build-base postgresql-dev libffi-dev zlib-dev jpeg-dev

FROM buildbase as pipdownload
# Set environment variables
ENV PYTHONUNBUFFERED 1
COPY ./requirements.txt /code/requirements.txt
RUN pip3 download -r /code/requirements.txt

FROM pipdownload as pip
RUN pip3 install -r /code/requirements.txt

from runbase as django
COPY --from=pip /usr/local/lib/python3.7/ /usr/local/lib/python3.7/
COPY --from=pip /usr/local/bin/ /usr/local/bin/
ENV PYTHONUNBUFFERED 1
RUN adduser -D -u 1000 django

from django as emptydjango
WORKDIR /code/
# Copy the current directory contents into the container at /code/
COPY . /code/
EXPOSE 8000
CMD ["/bin/sh", "/code/run.sh"]
