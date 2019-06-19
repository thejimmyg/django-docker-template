#!/bin/sh


RETRIES=99

until psql "$DATABASE_URL" -c "select 1" > /dev/null 2>&1 || [ $RETRIES -eq 0 ]; do
  echo "Waiting for postgres server, $((RETRIES--)) remaining attempts..."
  sleep 1
done
if [ ! -d "/code/mysite" ]; then
  echo "Creating the Django project ..."
  cd /tmp/
  /usr/local/bin/django-admin startproject mysite
  mv mysite/* /code/
  cd /code/
  echo "done."
fi
echo 'Fixing permissions on /code'
chown -R django /code
echo 'done'
su django
pip freeze > /code/freeze.txt
echo "Binding to $PORT"
# exec gunicorn mysite.wsgi:application --bind 0.0.0.0:8000 --workers 3
exec gunicorn -k gevent mysite.wsgi:application --bind "0.0.0.0:$PORT"