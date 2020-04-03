#!/bin/sh

# Exit if there are any errors
set -e

. run.common

echo "Binding to $PORT"
exec gunicorn -k gevent mysite.wsgi:application --bind "0.0.0.0:$PORT" --access-logfile - --error-logfile -
