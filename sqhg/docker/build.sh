#!/bin/bash

DEFAULT_PATH=$1

set -e

echo $MODE

if [ "$MODE" = "development" ]; then
    echo "Intall Development Dependencies"
    pip install -r ${DEFAULT_PATH}/development.txt
else
    echo "Intall Production Dependencies"
    pip install -r ${DEFAULT_PATH}/production.txt
fi
