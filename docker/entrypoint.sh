#!/bin/sh
set -e

echo "Waiting for PostgreSQL..."
until pg_isready -h db -U bacula -q; do
    sleep 1
done
echo "PostgreSQL is ready."

exec "$@"
