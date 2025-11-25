#!/bin/bash
# Update system packages
dnf update -y

# Install Docker
dnf install -y docker

# Start and enable Docker service
systemctl start docker
systemctl enable docker

# Add ec2-user to docker group
usermod -aG docker ec2-user

# Pull the latest image
docker pull omarleon/library-management:latest

# Run the container with RDS connection
docker run -d -p 8000:8000 \
  --name library-management-api \
  -e DATABASE_URL="mysql+mysqlconnector://<username>:<password>@<rds_endpoint>:3306/mydb" \
  omarleon/library-management:latest