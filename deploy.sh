#!/bin/env sh

IMAGE_NAME="budget-control-image"
CONTAINER_NAME="budget-control-container"

echo "Building Docker image..."

# Building a Docker image based on a Dockerfile
docker build -t $IMAGE_NAME .

# Checking if there is already a running container named $CONTAINER_NAME
if [ "$(docker ps -a --filter "name=$CONTAINER_NAME" --quiet)" ]; then
    # If the container is already running, then stop and delete it
    docker stop $CONTAINER_NAME
    docker rm $CONTAINER_NAME
fi

echo "Starting a container..."

# Launching a new container
docker run -d -p 5000:5000 --name $CONTAINER_NAME $IMAGE_NAME