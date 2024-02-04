#!/bin/env sh

# This test verifies that the application startup scripts work correctly and the container starts without problems

# Files checked by this test: deploy.sh -> Dockerfile -> run.sh

IMAGE_NAME="budget-control-image"
CONTAINER_NAME="budget-control-container"

echo "Running the deploy.sh script..."

./deploy.sh

sleep 15s

if [ "$(docker ps --all --filter "name=$CONTAINER_NAME" --quiet)" ]; then
  echo "Container created: OK"
else
  echo "Container created: FAILED"
fi

if [ "$(docker inspect --filter '{{.State.Running}}' $CONTAINER_NAME)" = "true" ]; then
  echo "Container started: OK"
  docker stop $CONTAINER_NAME
else
  echo "Container started: FAILED"
  exit 1
fi

sleep 15s

if [ "$(docker inspect --filter '{{.State.Running}}' $CONTAINER_NAME)" = "false" ]; then
  echo "Container stopped: OK"
  echo "Removing a container and image from the system..."
  docker rm $CONTAINER_NAME
  docker image rm $IMAGE_NAME
  exit 0
else
  echo "Container stopped: FAILED"
  exit 1
fi