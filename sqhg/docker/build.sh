#!/bin/bash

DEFAULT_PATH=$1

set -e

echo $MODE

if [ "$MODE" = "development" ]; then
    echo "Installing Development Dependencies"
    pip install -r ${DEFAULT_PATH}/development.txt
else
    echo "Installing Production Dependencies"
    pip install -r ${DEFAULT_PATH}/production.txt
fi
