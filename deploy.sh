#!/bin/env sh

IMAGE_NAME="budget-control-image"
CONTAINER_NAME="budget-control-container"

echo "Building Docker image..."

# Building a Docker image based on a Dockerfile
docker build --tag $IMAGE_NAME .

# Checks if a Docker container with a specific name "$CONTAINER_NAME" exists
if [ "$(docker ps --all --filter "name=$CONTAINER_NAME" --quiet)" ]; then
    # If the container is already running, then stop and delete it
    docker stop $CONTAINER_NAME
    docker rm $CONTAINER_NAME
fi

echo "Starting a container..."

# Launching a new container
docker run --detach --publish 5000:5000 --name $CONTAINER_NAME $IMAGE_NAME