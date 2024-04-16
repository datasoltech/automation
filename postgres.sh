#!/bin/bash

# Variables
VM_NAME="my-postgres-$(date +'%Y%m%d%H%M%S')"
MACHINE_TYPE="e2-medium"
REGION="asia-south1-b"
IMAGE_FAMILY="debian-10"
DOCKERFILE_CONTENT="# Use the official PostgreSQL image from Docker Hub
FROM postgres:latest

# Install the necessary packages to build the extension
RUN apt-get update && \
    apt-get install -y \
    build-essential \
    postgresql-server-dev-all \
    git

# Clone the pg_vector repository and build the extension
RUN git clone https://github.com/postgrespro/pg_vector.git /tmp/pg_vector && \
    cd /tmp/pg_vector && \
    make USE_PGXS=1 && \
    make USE_PGXS=1 install

# Set environment variables for the PostgreSQL database
ENV POSTGRES_DB=mydatabase \
    POSTGRES_USER=rooot \
    POSTGRES_PASSWORD=BinRoot@123

# Expose the PostgreSQL port
EXPOSE 5432


"
sleep 25

# Create VM instance
gcloud compute instances create $VM_NAME \
    --machine-type=$MACHINE_TYPE \
    --zone=$REGION \
    --image-family=$IMAGE_FAMILY \
    --image-project=debian-cloud
sleep 20 

# SSH into the VM and create Dockerfile

gcloud compute ssh $VM_NAME --zone=$REGION --command=" sudo apt install -y docker.io"

gcloud compute ssh $VM_NAME --zone=$REGION --command="echo '$DOCKERFILE_CONTENT' > Dockerfile"

# Build Docker image
gcloud compute ssh $VM_NAME --zone=$REGION --command="sudo docker build -t my-postgres-image ."

# Run Docker container
gcloud compute ssh $VM_NAME --zone=$REGION --command="sudo docker run -d --name my-postgres-container -p 5432:5432 my-postgres-image "
