#!/bin/bash

# Generate a random name for the container using uuidgen
container_name=$(uuidgen)

# Build the Docker image with your project code and unit tests
docker build -t dungeon-backend -f Dockerfile.backend .

# Run the Docker container with the unit tests and attach the output
docker run --tty --rm --name "$container_name" -p 5000:5000 dungeon-backend

# Exit the script with the exit code of the container
exit $?
