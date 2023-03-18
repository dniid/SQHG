#!/bin/bash

set -e

echo "${GITHUB_ACTION_PATH}/run.sh"
echo $SCRIPT
echo ${SCRIPT} >> ${GITHUB_ACTION_PATH}/run.sh

docker build ${GITHUB_ACTION_PATH} --build-arg IMAGE=$IMAGE -t temp-${GITHUB_RUN_ID}

docker run --rm \
  -v ${GITHUB_WORKSPACE}:"/github/workspace" \
  -u root:root \
  -e MODE=ci \
  -w /github/workspace \
  temp-${GITHUB_RUN_ID}
