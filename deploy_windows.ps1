# Image and container name
$IMAGE_NAME="budget-control-image"
$CONTAINER_NAME="budget-control-container"

Write-Host "Building Docker image..."

# Building a Docker image based on a Dockerfile
docker build -t $IMAGE_NAME .

# Checking if there is already a running container named $CONTAINER_NAME
$containerExists = docker ps -a --filter "name=$CONTAINER_NAME" -q
if ($containerExists) {
    # If the container is already running, then stop and delete it
    docker stop $CONTAINER_NAME
    docker rm $CONTAINER_NAME
}

Write-Host "Starting a container..."

# Launching a new container
docker run -d -p 5000:5000 --name $CONTAINER_NAME $IMAGE_NAME
