#!/bin/bash

: ${TAIGA_SLEEP:=5}

echo "Waiting for $TAIGA_SLEEP seconds..."
sleep $TAIGA_SLEEP

if [ -z "$TAIGA_SKIP_DB_CHECK" ]; then

  echo "Checking database..."
  TRIALS=0
  while :
    python /taiga/checkdb.py
    DB_CHECK_STATUS=$?
    [ $DB_CHECK_STATUS -eq 1 ] && [ $TRIALS -lt 6 ] || break
  do
    ((TRIALS++))
    echo "Could not connect to PostgreSQL database, will try again in 10 seconds..."
    sleep 10
  done

  if [ $DB_CHECK_STATUS -eq 1 ]; then
    echo "Failed to connect to database server or database does not exist."
    exit 1
  elif [ $DB_CHECK_STATUS -eq 2 ]; then
    echo "Configuring initial database..."
    python manage.py migrate --noinput
    python manage.py loaddata initial_user
    python manage.py loaddata initial_project_templates
    python manage.py loaddata initial_role
    python manage.py compilemessages
    python manage.py collectstatic --noinput
  fi
fi

# Look for static folder, if it does not exist, then generate it
if [ ! -d "/usr/src/taiga-back/static" ]; then
  python manage.py collectstatic --noinput
fi

# Automatically replace "TAIGA_HOSTNAME" with the environment variable
echo "Replacing TAIGA_HOSTNAME in conf.json..."
sed -i "s/TAIGA_HOSTNAME/$TAIGA_HOSTNAME/g" /taiga/conf.json

# Look to see if we should set the "eventsUrl"
if [ ! -z "$TAIGA_EVENTS_ENABLED" ]; then
  echo "Setting eventsUrl in conf.json..."
  sed -i "s/eventsUrl\": null/eventsUrl\": \"ws:\/\/$TAIGA_HOSTNAME\/events\"/g" /taiga/conf.json
fi

# Handle enabling/disabling SSL
if [ "$TAIGA_SSL" = "True" ]; then
  echo "Enabling SSL in conf.json..."
  sed -i "s/http:\/\//https:\/\//g" /taiga/conf.json
  sed -i "s/ws:\/\//wss:\/\//g" /taiga/conf.json
fi

# Start services:
echo "Starting nginx..."
service nginx start

if [ ! -z "$TAIGA_EVENTS_ENABLED" ]; then
  echo "Starting celery..."
  C_FORCE_ROOT=1 celery -A taiga worker -c 4 2> /dev/stderr &
fi

echo "Starting taiga-back..."
exec "$@"
