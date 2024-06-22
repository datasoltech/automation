



#!/bin/bash

# Variables
VM_NAME="alloydbomni-$(date +'%Y%m%d%H%M%S')"
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
gcloud compute ssh $VM_NAME --zone=$ZONE --command="sudo docker run -d \
    --name my-omni \
    -e POSTGRES_PASSWORD=BinRoot@123 \
    -p 5432:5432 \
    google/alloydbomni" > /dev/null 2>&1

# Get external IP address
EXTERNAL_IP=$(gcloud compute instances describe $VM_NAME --zone=$ZONE --format='get(networkInterfaces[0].accessConfigs[0].natIP)')

# Print instance name and external IP address
echo "Instance_Name: $VM_NAME"
echo "External_IP: $EXTERNAL_IP"

# Print MySQL database configuration
echo "ALLOYDBOMINI_DATABASE: my_database"
echo "ALLOYDBOMINI_USER: postgres"
echo "ALLOYDBOMINI_PASSWORD: BinRoot@123"
