#!/bin/env sh

# This test verifies that the application startup scripts work correctly and the container starts without problems

echo ">>> Running Docker Compose..."
docker compose up --detach --build

echo ">>> Pause 5s..."
sleep 5 # time to start the containers

container_status=$(docker compose ps)

if ! echo "$container_status" | grep -q "Up"; then
    echo ">>> Status: FAILED"
    echo ">>> Containers were not started"
    exit 1
fi

echo ">>> Stopping Docker Compose..."
docker compose down --volumes

echo ">>> Pause 5s..."
sleep 5 # time to stop the containers

container_status=$(docker compose ps -q)

if [ -n "$container_status" ]; then
    echo ">>> Status: FAILED"
    echo ">>> Containers were not stopped"
    exit 1
fi

echo ">>> Status: OK"
exit 0