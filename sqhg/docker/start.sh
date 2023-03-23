#!/bin/sh

set -e
set -x

echo "Starting SQHG backend as `whoami`"
if [ "$MODE" = "development" ]; then
    uvicorn main:app --host $HOST --port $PORT --reload
else
    mkdir -p $LOGS_ROOT/sqhg_data.log
    gunicorn --workers 4 --timeout 300 \
    --bind $HOST:$PORT main:app
fi
