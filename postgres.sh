#!/bin/bash

# Variables
VM_NAME="my-postgres-$(date +'%Y%m%d%H%M%S')"
MACHINE_TYPE="e2-medium"
REGION="asia-south1-b"
IMAGE_FAMILY="debian-10"





# Create VM instance
gcloud compute instances create $VM_NAME \
    --machine-type=$MACHINE_TYPE \
    --zone=$REGION \
    --image-family=$IMAGE_FAMILY \
    --image-project=debian-cloud
sleep 20 

# SSH into the VM and create Dockerfile

gcloud compute ssh $VM_NAME --zone=$REGION --command=" sudo apt install -y docker.io"

gcloud compute ssh $VM_NAME --zone=$REGION --command=" docker run -d \
    --name postgres-db \
    -e POSTGRES_USER=rooot \
    -e POSTGRES_PASSWORD=BinRoot@123 \
    -p 5432:5432 \
    postgres:latest
 " 
