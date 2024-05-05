#!/bin/bash

# Variables
VM_NAME="my-sql-$(date +'%Y%m%d%H%M%S')"
MACHINE_TYPE="e2-medium"
REGION="us-central1-a"
IMAGE_FAMILY="debian-10"
DOCKERFILE_CONTENT="# Use the official MySQL image from Docker Hub
FROM mysql:latest

# Set the root password (change it to your desired password)
ENV MYSQL_ROOT_PASSWORD=root_password

# (Optional) Create a database and user
ENV MYSQL_DATABASE=my_database
ENV MYSQL_USER=rooot
ENV MYSQL_PASSWORD=BinRoot@123

# (Optional) Populate the database with SQL scripts
# COPY ./sql-scripts /docker-entrypoint-initdb.d/
"

# Create VM instance without printing output
gcloud compute instances create $VM_NAME \
    --machine-type=$MACHINE_TYPE \
    --zone=$REGION \
    --image-family=$IMAGE_FAMILY \
    --image-project=debian-cloud \
    >/dev/null 2>&1

sleep 25

# SSH into the VM and create Dockerfile without printing output
gcloud compute ssh $VM_NAME --zone=$REGION --command="sudo apt install -y docker.io" >/dev/null 2>&1

gcloud compute ssh $VM_NAME --zone=$REGION --command="echo '$DOCKERFILE_CONTENT' > Dockerfile" >/dev/null 2>&1

# Build Docker image without printing output
gcloud compute ssh $VM_NAME --zone=$REGION --command="sudo docker build -t mysql_container ." >/dev/null 2>&1

# Run Docker container without printing output
gcloud compute ssh $VM_NAME --zone=$REGION --command="sudo docker run -d --name mysql_container -p 3306:3306 mysql_container" >/dev/null 2>&1



# Get external IP address
EXTERNAL_IP=$(gcloud compute instances describe $VM_NAME --zone=$REGION --format='get(networkInterfaces[0].accessConfigs[0].natIP)')

# Print instance name and external IP address
echo "Instance_Name: $VM_NAME"
echo "External_IP: $EXTERNAL_IP"

# Print MySQL database configuration
echo "MYSQL_DATABASE: my_database"
echo "MYSQL_USER: rooot"
echo "MYSQL_PASSWORD: BinRoot@123"
