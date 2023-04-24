#!/usr/bin/env sh

set -eu

usage() {
    echo "Usage: $0 [-d] [-m] [-q] [-w]" 1>&2
    echo "Options: " 1>&2
    echo "-d: Run as development mode" 1>&2
    echo "-m: Run migration" 1>&2
    echo "-q: Quit without running server" 1>&2
    echo "-w: Wait for database to start" 1>&2
    exit 1
}

WAIT=0
QUIT=0
MIGRATION=0
ENVIRONMENT=prod

while getopts :dwmqh OPT
do
    case $OPT in
    d)  ENVIRONMENT=dev
        ;;
    w)  WAIT=1
        ;;
    m)  MIGRATION=1
        ;;
    q)  QUIT=1
        ;;
    h)  usage
        ;;
    \?) usage
        ;;
    esac
done

if [ "$WAIT" = "1" ]; then
    echo "Waiting for db"
    dockerize -wait tcp://$DATABASE_HOST:$DATABASE_PORT -timeout 480s
fi

if [ "$MIGRATION" = "1" ]; then
    echo "Running migration"
    python manage.py migrate
fi

if [ "$QUIT" = "1" ]; then
    exit 0
fi

if [ "${ENVIRONMENT:-}" = "dev" ]; then
    python manage.py runserver 0.0.0.0:80
elif [ "${ENVIRONMENT:-}" = "prod" ]; then
    python manage.py update_events_data
fi
