#!/bin/bash

if [ ! -f "/opt/airflow/airflow.db" ]; then
  airflow db init
fi

airflow users list | grep -q 'admin' || \
airflow users create \
  --username admin \
  --firstname Admin \
  --lastname User \
  --role Admin \
  --email admin@example.com \
  --password admin

exec "$@"
