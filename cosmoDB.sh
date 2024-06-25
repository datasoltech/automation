#!/bin/bash

# Variables
VM_NAME="cosmoDB-$(date +'%Y%m%d%H%M%S')"
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

# Run Docker container in detached mode
gcloud compute ssh $VM_NAME --zone=$ZONE --command="sudo docker pull mcr.microsoft.com/cosmosdb/linux/azure-cosmos-emulator" > /dev/null 2>&1
gcloud compute ssh $VM_NAME --zone=$ZONE --command="sudo docker run -p 8081:8081 -p 10250:10250 -p 10251:10251 -p 10252:10252 -p 10253:10253 -p 10254:10254 -d --name=cosmosdb-emulator mcr.microsoft.com/cosmosdb/linux/azure-cosmos-emulator" > /dev/null 2>&1

# Get external IP address
EXTERNAL_IP=$(gcloud compute instances describe $VM_NAME --zone=$ZONE --format='get(networkInterfaces[0].accessConfigs[0].natIP)')

# Print instance name and external IP address
echo "Instance_Name: $VM_NAME"
echo "External_IP: $EXTERNAL_IP"

# Print MySQL database configuration
echo "cosmoDB_DATABASE: my_database"
echo "cosmoDB_USER: rooot"
echo "cosmoDB_PASSWORD: BinRoot@123"
