#!/bin/bash

# Variables
VM_NAME="mysql-$(date +'%Y%m%d%H%M%S')"
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
gcloud compute ssh $VM_NAME --zone=$ZONE --command="sudo docker run --name mysql-container \
  -e MYSQL_ROOT_PASSWORD=BinRoot@123 \
  -e MYSQL_DATABASE=my_database \
  -e MYSQL_USER=rooot \
  -e MYSQL_PASSWORD=BinRoot@123 \
  -p 3306:3306 \
  -v mysql-data:/var/lib/mysql \
  --restart unless-stopped \
  -d mysql:latest
" > /dev/null 2>&1

# Get external IP address
EXTERNAL_IP=$(gcloud compute instances describe $VM_NAME --zone=$ZONE --format='get(networkInterfaces[0].accessConfigs[0].natIP)')

# Print instance name and external IP address
echo "Instance_Name: $VM_NAME"
echo "External_IP: $EXTERNAL_IP"

# Print MySQL database configuration
echo "MYSQL_DATABASE: my_database"
echo "MYSQL_USER: rooot"
echo "MYSQL_PASSWORD: BinRoot@123"
