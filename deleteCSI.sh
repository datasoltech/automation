#!/bin/bash

# Get Cloud SQL instance name from command-line argument
INSTANCE_NAME="$1"

# Check if the instance name is provided
if [ -z "$INSTANCE_NAME" ]; then
  echo "Usage: $0 <instance_name>"
  exit 1
fi

# Delete the Cloud SQL instance
yes | gcloud sql instances delete "$INSTANCE_NAME" --quiet

# Check if the deletion was successful
if [ $? -eq 0 ]; then
  echo "Cloud SQL instance '$INSTANCE_NAME' deleted successfully."
else
  echo "Error: Failed to delete Cloud SQL instance '$INSTANCE_NAME'."
fi
