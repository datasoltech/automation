#!/bin/bash

# Set variables
PROJECT_ID="genaiexperiments-1"
REGION="us-central1"
INSTANCE_NAME="cloudsqlp-$(date +'%Y%m%d%H%M%S')"
DATABASE_VERSION="POSTGRES_9_6"
DATABASE_TIER="db-f1-micro"  # Change the tier to a valid one
USERNAME="postgres"
USER_PASSWORD="BinRoot@123"  # Change the password to your desired one

# Create Cloud SQL instance with a valid name
# Convert uppercase to lowercase and replace non-alphanumeric characters with hyphens
#INSTANCE_NAME=$(echo "$INSTANCE_NAME" | tr '[:upper:]' '[:lower:]' | sed 's/[^a-z0-9]/-/g')

# Create Cloud SQL instance
nohup gcloud sql instances create $INSTANCE_NAME \
    --project=$PROJECT_ID \
    --region=$REGION \
    --database-version=$DATABASE_VERSION \
    --tier=$DATABASE_TIER > /dev/null 2>&1 &   # Redirect output to /dev/null

# Set root password for Cloud SQL instance
# You might need to have sufficient permissions to execute this command
gcloud sql users set-password root \
    --project=$PROJECT_ID \
    --instance=$INSTANCE_NAME \
    --password=$USER_PASSWORD > /dev/null 2>&1  # Redirect output to /dev/null

sleep 50

# Get public IP address of the PostgreSQL instance
PUBLIC_IP=$(gcloud sql instances describe $INSTANCE_NAME --project=$PROJECT_ID --format="value(ipAddresses[0].ipAddress)")
OUTGOING_IP=$(gcloud sql instances describe $INSTANCE_NAME --project=$PROJECT_ID --format="value(ipAddresses[1].ipAddress)")

# Print instance name and external IP address
echo "Instance_Name: $INSTANCE_NAME"
echo "PUBLIC_IP: $PUBLIC_IP"
echo "OUTGOING_IP: $OUTGOING_IP"

# Print PostgreSQL database configuration
echo "POSTGRES_DATABASE: "
echo "POSTGRES_USER: postgres"
echo "POSTGRES_PASSWORD: $USER_PASSWORD"

