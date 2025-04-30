#!/bin/bash

#Variables
CONTAINER_NAME="portfolio_container"
IMAGE_NAME="portfolio"
DOCKERFILE_PATH="."
PORT_MAPPING="80:80"

# Check if the user is root
if [ "$(id -u)" -ne 0 ]; then
    echo "This script must be run as root. Please use sudo."
    exit 1
fi

# Check if Docker is running
check_docker() {
    if ! docker info > /dev/null 2>&1; then
        echo "Docker is not running. Please start Docker and try again."
        exit 1
    fi
}

# Stop and remove existing container
stop_container() {
    echo "Stopping Docker container..."
    docker stop $CONTAINER_NAME 2> /dev/null || true
    docker rm $CONTAINER_NAME 2> /dev/null || true
    echo "Container stopped"
}

# Build the Docker image
build_image() {
    echo "Building Docker image..."
    docker build -t $IMAGE_NAME $DOCKERFILE_PATH
    if [ $? -ne 0 ]; then
        echo "Failed to build Docker image. Are you in the right directory with a valid Dockerfile?"
        exit 1
    fi
    echo "Image built successfully"
}

# Deploy the Docker container
deploy_container() {
    echo "Deploying Docker container..."
    docker run -d --name $CONTAINER_NAME -p $PORT_MAPPING $IMAGE_NAME
    if [ $? -ne 0 ]; then
        echo "Failed to deploy Docker container."
        exit 1
    fi
    echo "Container deployed successfully"
}

# Full redeploy
redeploy() {
    check_docker
    stop_container
    build_image
    deploy_container
}

status() {
    echo "Container Status:"
    docker ps -a --filter "name=$CONTAINER_NAME" --format "table {{.Names}}\t{{.Status}}"
}

case "$1" in
    redeploy)
        redeploy
        ;;
    stop)
        stop_container
        ;;
    build)
        check_docker
        build_image
        ;;
    deploy)
        check_docker
        deploy_container
        ;;
    status)
        check_docker
        status
        ;;
    *)
        echo "Usage: $0 {redeploy|stop|build|deploy|status}"
        echo "  redeploy  - Stop existing container, build a new image, and deploy"
        echo "  stop      - Stop the existing Docker container"
        echo "  build     - Build the Docker image"
        echo "  deploy    - Deploy the Docker container"
        echo "  status    - Show the status of the Docker container"
        echo "Example: $0 redeploy"
        echo "This script must be run as root. Please use sudo."
        echo "Note: Ensure Docker is installed and running."
        exit 1
        ;;
esac