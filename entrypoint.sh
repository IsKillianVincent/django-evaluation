#!/bin/bash
# Merci Stackoverflow

echo "Waiting for Postgres..."
while ! nc -z $DB_HOST $DB_PORT; do
  sleep 1
done
echo "Postgres is ready"

python manage.py migrate --noinput
python manage.py collectstatic --noinput

# Start server
exec "$@"