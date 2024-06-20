#!/bin/bash

# Variables
VM_NAME="postgres-$(date +'%Y%m%d%H%M%S')"
MACHINE_TYPE="e2-medium"
ZONE="us-central1-a"
IMAGE_FAMILY="debian-12"

# Create VM instance
gcloud compute instances create $VM_NAME \
    --machine-type=$MACHINE_TYPE \
    --zone=$ZONE \
    --image-family=$IMAGE_FAMILY \
    --image-project=debian-cloud > /dev/null 2>&1

sleep 20

# Install Docker
gcloud compute ssh $VM_NAME --zone=$ZONE --command="sudo apt update && sudo apt install -y docker.io" > /dev/null 2>&1

# Run Docker container
gcloud compute ssh $VM_NAME --zone=$ZONE --command="sudo docker run --name my-postgres -e POSTGRES_PASSWORD=BinRoot@123 -e POSTGRES_USER=rooot -e POSTGRES_DB=my_database -p 5432:5432 -d postgres" > /dev/null 2>&1

# Get external IP address
EXTERNAL_IP=$(gcloud compute instances describe $VM_NAME --zone=$ZONE --format='get(networkInterfaces[0].accessConfigs[0].natIP)')

# Print instance name and external IP address
echo "Instance_Name: $VM_NAME"
echo "External_IP: $EXTERNAL_IP"

# Print MySQL database configuration
echo "POSTGRES_DATABASE: my_database"
echo "POSTGRES_USER: postgres"
echo "POSTGRES_PASSWORD: BinRoot@123"
