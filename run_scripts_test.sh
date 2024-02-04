#!/bin/env sh

# This test verifies that the application startup scripts work correctly and the container starts without problems

# Files checked by this test: deploy.sh -> Dockerfile -> run.sh

IMAGE_NAME="budget-control-image"
CONTAINER_NAME="budget-control-container"

./deploy.sh

sleep 5s

if [ "$(docker inspect -f '{{.State.Running}}' $CONTAINER_NAME)" = "true" ]; then
  docker stop $CONTAINER_NAME
else
  exit 1
fi

sleep 5s

if [ "$(docker inspect -f '{{.State.Running}}' $CONTAINER_NAME)" = "false" ]; then
  docker rm $CONTAINER_NAME
  docker image rm $IMAGE_NAME

  exit 0
else
  exit 1
fi