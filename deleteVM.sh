#!/bin/bash

# Get instance name from command-line argument
instance_name="$1"

# Check if instance name is provided
if [ -z "$instance_name" ]; then
  echo "Usage: $0 <instance_name>"
  exit 1
fi

# Set project and zone
project="genaiexperiments-1"
zone="us-central1-a"

# Delete VM instance
yes | gcloud compute instances delete "$instance_name" --project "$project" --zone "$zone" --quiet

# Check if deletion was successful
if [ $? -eq 0 ]; then
  echo "VM instance $instance_name successfully deleted."
else
  echo "Failed to delete VM instance $instance_name."
fi
