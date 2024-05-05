#!/bin/bash

# Generate a timestamp or a random string
TIMESTAMP=$(date +'%Y%m%d%H%M%S')
# Or use a random string (requires `uuidgen` command)
# RANDOM_STRING=$(uuidgen | tr '[:upper:]' '[:lower:]')

# Combine the timestamp/random string with a prefix
VM_NAME="postgres-$TIMESTAMP"
# Or use the random string directly
# VM_NAME="my-debian-12-instance-$RANDOM_STRING"

MACHINE_TYPE="e2-medium"
REGION="us-central1"
ZONE="${REGION}-a"  # Choose a zone within the region
IMAGE_PROJECT="debian-cloud"
IMAGE_FAMILY="debian-12"

# Create VM instance
gcloud compute instances create $VM_NAME \
    --machine-type=$MACHINE_TYPE \
    --zone=$ZONE \
    --image-family=$IMAGE_FAMILY \
    --image-project=$IMAGE_PROJECT \
    >/dev/null 2>&1

sleep 25

# SSH into the VM and install Docker
gcloud compute ssh $VM_NAME --zone=$ZONE --command="sudo apt update && sudo apt install -y docker.io" >/dev/null 2>&1

# Run PostgreSQL container inside the VM
gcloud compute ssh $VM_NAME --zone=$ZONE --command="sudo docker run -d \
    --name postgres-db \
    -e POSTGRES_USER=rooot \
    -e POSTGRES_PASSWORD=BinRoot@123 \
    -p 5432:5432 \
    postgres:latest" >/dev/null 2>&1


# Get external IP address
EXTERNAL_IP=$(gcloud compute instances describe $VM_NAME --zone=$ZONE --format='get(networkInterfaces[0].accessConfigs[0].natIP)')

# Print instance name and external IP address
echo "Instance_Name: $VM_NAME"
echo "External_IP: $EXTERNAL_IP"

# Print MySQL database configuration
echo "POSTGRES_DATABASE: my_database"
echo "POSTGRES_USER: rooot"
echo "POSTGRES_PASSWORD: BinRoot@123"
