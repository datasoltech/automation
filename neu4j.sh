#!/bin/bash

# Variables
# VM_NAME="my-neo4j-$(date +'%Y%m%d%H%M%S')"
# MACHINE_TYPE="e2-medium"
# REGION="asia-south1-b"
# IMAGE_FAMILY="debian-10"
#
# # Create VM instance
# gcloud compute instances create $VM_NAME \
#     --machine-type=$MACHINE_TYPE \
#         --zone=$REGION \
#             --image-family=$IMAGE_FAMILY \
#                 --image-project=debian-cloud
#
#                 sleep 20 
#
#
#                 gcloud compute ssh $VM_NAME --zone=$REGION --command="sudo apt install -y docker.io"
#
#
#
#                 # Run Docker container
#                 gcloud compute ssh $VM_NAME --zone=$REGION --command=" docker run \
#                     --restart always \
#                         --publish=7474:7474 --publish=7687:7687 \
#                             --env NEO4J_AUTH=neo4j/BinRoot@123 \
#                                 neo4j:5.19.0"
