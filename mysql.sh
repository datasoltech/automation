# Variables
VM_NAME="my-sql-$(date +'%Y%m%d%H%M%S')"
MACHINE_TYPE="e2-medium"
REGION="asia-south1-b"
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

# Create VM instance
gcloud compute instances create $VM_NAME \
    --machine-type=$MACHINE_TYPE \
    --zone=$REGION \
    --image-family=$IMAGE_FAMILY \
    --image-project=debian-cloud

sleep 25

# SSH into the VM and create Dockerfile

gcloud compute ssh $VM_NAME --zone=$REGION --command=" sudo apt install -y docker.io"

gcloud compute ssh $VM_NAME --zone=$REGION --command="echo '$DOCKERFILE_CONTENT' > Dockerfile"

# Build Docker image
gcloud compute ssh $VM_NAME --zone=$REGION --command="sudo docker build -t mysql_container ."

# Run Docker container
gcloud compute ssh $VM_NAME --zone=$REGION --command="sudo docker run -d --name mysql_container -p 3306:3306 mysql_container"
