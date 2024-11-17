#!/bin/bash

# Check if app name is provided
if [ -z "$1" ]; then
    echo "Usage: ./create_app.sh [APP_NAME]"
    exit 1
fi

APP_NAME=$1

# Create project structure
mkdir -p $APP_NAME/{frontend,backend,database,scripts,.github/workflows}

# Initialize frontend
cd $APP_NAME/frontend
npx create-react-app .
rm -rf .git

# Initialize backend
cd ../backend
python -m venv venv
source venv/bin/activate
pip install django djangorestframework django-cors-headers psycopg2-binary
django-admin startproject core .
python manage.py startapp api

# Create database initialization script
cd ../database
echo "CREATE DATABASE $APP_NAME;" > init.sql

# Copy configuration files
cd ..
curl -o docker-compose.yml https://raw.githubusercontent.com/yourusername/saas-platform/main/docker-compose.yml
curl -o frontend/Dockerfile https://raw.githubusercontent.com/yourusername/saas-platform/main/frontend/Dockerfile
curl -o backend/Dockerfile https://raw.githubusercontent.com/yourusername/saas-platform/main/backend/Dockerfile
curl -o .github/workflows/ci.yml https://raw.githubusercontent.com/yourusername/saas-platform/main/.github/workflows/ci.yml

# Initialize git repository
git init
git add .
git commit -m "Initial commit for $APP_NAME"

echo "SAAS application '$APP_NAME' has been created successfully!"
echo "Next steps:"
echo "1. Update configuration files with your specific settings"
echo "2. Push to your repository"
echo "3. Run 'docker-compose up' to start the application"