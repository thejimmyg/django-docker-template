#!/bin/sh

# Exit if there are any errors
set -e

RETRIES=99

until psql "$DATABASE_URL" -c "select 1" > /dev/null 2>&1 || [ $RETRIES -eq 0 ]; do
  echo "Waiting for postgres server, $((RETRIES--)) remaining attempts..."
  sleep 2
done
# Exit if we still can't connect after waiting about 200 seconds.
psql "$DATABASE_URL" -c "select 1"
echo 'Fixing permissions on /code'
chown -R django /code
echo 'done'
su django
# Just so we know exactly what versions we are using.
pip freeze > /code/freeze.txt
echo "Binding to $PORT"
exec gunicorn -k gevent mysite.wsgi:application --bind "0.0.0.0:$PORT"
