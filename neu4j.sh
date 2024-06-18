#!/bin/bash

# Variables
VM_NAME="my-neo4j-$(date +'%Y%m%d%H%M%S')"
MACHINE_TYPE="e2-medium"
REGION="asia-south1-b"
IMAGE_FAMILY="debian-10"

# Create VM instance
gcloud compute instances create $VM_NAME \
    --machine-type=$MACHINE_TYPE \
    --zone=$REGION \
    --image-family=$IMAGE_FAMILY \
    --image-project=debian-cloud > /dev/null 2>&1

sleep 20

# Install Docker
gcloud compute ssh $VM_NAME --zone=$REGION --command="sudo apt install -y docker.io" > /dev/null 2>&1

# Run Docker container
gcloud compute ssh $VM_NAME --zone=$REGION --command="sudo docker run \
    --restart always \
    --publish=7474:7474 --publish=7687:7687 \
    --env NEO4J_AUTH=neo4j/BinRoot@123 \
    neo4j:5.19.0" > /dev/null 2>&1


# Get external IP address
EXTERNAL_IP=$(gcloud compute instances describe $VM_NAME --zone=$ZONE --format='get(networkInterfaces[0].accessConfigs[0].natIP)')

# Print instance name and external IP address
echo "Instance_Name: $VM_NAME"
echo "External_IP: $EXTERNAL_IP"

# Print MySQL database configuration
echo "NEU4J_DATABASE: "
echo "NEU4J_USER: neu4j"
echo "NEU4J_PASSWORD: BinRoot@123"
