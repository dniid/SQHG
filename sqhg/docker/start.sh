#!/bin/bash

set -e
set -x

echo "Checking migrations..."
if [[ $(alembic check) =~ "FAILED: New upgrade"* ]]; then
    echo "Generating migrations..."
    alembic-autogen-check --config ./alembic.ini ||
    file_count=$(ls -1 alembic/versions | wc -l)
    file_count=$(printf "%03d" "$file_count")
    alembic revision --autogenerate -m "$file_count"
fi

echo "Applying migrations..."
alembic upgrade head

echo "Starting SQHG backend as `whoami`"
if [ "$MODE" = "development" ]; then
    uvicorn main:app --host $HOST --port $PORT --reload
else
    mkdir -p $LOGS_ROOT/sqhg_data.log
    gunicorn --workers 4 --timeout 300 \
    -k uvicorn.workers.UvicornWorker \
    --bind $HOST:$PORT main:app
fi
