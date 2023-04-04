#!/bin/bash -x

PROJECT_DIR=..
APP_NAME=waseda-moodle-scheduler

cd "$(dirname "$0")" || exit

# init environment variables
#cp -v ${PROJECT_DIR}/${APP_NAME}/.env.example ${PROJECT_DIR}/${APP_NAME}/.env

# init mysql log files
mkdir -p ${PROJECT_DIR}/log/mysql
touch ${PROJECT_DIR}/log/mysql/mysqld.log

# init log file permission
find ${PROJECT_DIR}/log -type f -print | xargs chmod 666
