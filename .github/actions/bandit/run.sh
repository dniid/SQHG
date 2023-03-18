#!/bin/sh
set -e
echo "############################################"
echo "Checking security with Bandit..."
bandit -r $INPUT_BASEPATH/
echo "############################################"
