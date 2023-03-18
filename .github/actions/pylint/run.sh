#!/bin/sh
set -e
echo "############################################"
echo "Checking for errors on Pylint..."
pylint --rcfile=$INPUT_CONFIGURATIONFILE $INPUT_BASEPATH/
echo "############################################"
