#!/bin/bash

# Update system
sudo apt-get update
sudo apt-get upgrade -y

# Install Docker and Docker Compose
sudo apt-get install -y apt-transport-https ca-certificates curl software-properties-common
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -
sudo add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable"
sudo apt-get update
sudo apt-get install -y docker-ce docker-compose

# Install Nginx
sudo apt-get install -y nginx

# Copy Nginx configuration
sudo cp nginx.conf /etc/nginx/sites-available/default
sudo systemctl restart nginx

# Clone your repository 
git clone http://github.com/TESTMECS/mlapi
cd http://github.com/TESTMECS/mlapi

# Start Docker services
sudo docker compose up -d 