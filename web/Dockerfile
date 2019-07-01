FROM python:3.7.3
RUN apt-get update -y
RUN apt-get install -y postgresql-client
RUN pip3 install --upgrade pip
ENV PYTHONUNBUFFERED 1
COPY ./requirements.txt /code/requirements.txt
RUN pip3 install -r /code/requirements.txt
RUN adduser --no-create-home --uid 2000 --disabled-password django --gecos ""
USER django
WORKDIR /code/
COPY . /code/
EXPOSE 8000
CMD ["/bin/sh", "/code/run.sh"]
