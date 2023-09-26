#!/bin/env sh

# Image and container name
IMAGE_NAME="budget-control-image"
CONTAINER_NAME="budget-control-container"

# Building a Docker image based on a Dockerfile
docker build -t $IMAGE_NAME .


