#!/bin/sh

set -e

echo 'Starting Nginx ...'
nginx # -g "daemon off;"
echo 'done.'

echo 'Handing over to cron.'
# Run cron in the foreground so that nginx can be safely reloaded without exiting this script.
crond -f -l 8 -L /dev/stdout 
