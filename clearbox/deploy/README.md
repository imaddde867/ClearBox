# ClearBox Deployment Guide

This directory contains deployment scripts and configuration files to help you deploy ClearBox to AWS.

## Table of Contents

1. [Prerequisites](#prerequisites)
2. [Pre-Deployment Checklist](#pre-deployment-checklist)
3. [AWS Resource Setup](#aws-resource-setup)
4. [Frontend Deployment](#frontend-deployment)
5. [Backend Deployment](#backend-deployment)
6. [Database Migration](#database-migration)
7. [Domain Configuration](#domain-configuration)
8. [Monitoring Setup](#monitoring-setup)
9. [Maintenance](#maintenance)
10. [Troubleshooting](#troubleshooting)

## Prerequisites

- AWS CLI installed and configured
- SSH client installed
- AWS account with permissions to create required resources
- Registered domain name (optional, but recommended)
- Git installed

## Pre-Deployment Checklist

- [ ] Generate new secure keys for production
- [ ] Remove hardcoded secrets from configuration files
- [ ] Test the application locally with a PostgreSQL database
- [ ] Build the frontend production assets
- [ ] Update all dependencies to latest secure versions
- [ ] Run any database migrations

## AWS Resource Setup

### 1. Create EC2 Instance

1. Log in to AWS Management Console
2. Navigate to EC2
3. Launch a new EC2 instance:
   - Amazon Linux 2 AMI
   - t2.micro (free tier eligible)
   - Configure security group:
     - Allow SSH (port 22) from your IP
     - Allow HTTP (port 80) from anywhere
     - Allow HTTPS (port 443) from anywhere
     - Allow custom TCP (port 8000) from anywhere (API port)
   - Create/select a key pair and download the .pem file

### 2. Set Up RDS PostgreSQL

1. Navigate to RDS in AWS console
2. Create database:
   - Engine: PostgreSQL
   - Template: Free tier
   - DB instance size: db.t2.micro
   - Storage: 20 GB (or minimum allowed)
   - Multi-AZ: No (for free tier)
   - Configure security group:
     - Allow PostgreSQL (port 5432) from your EC2 security group

### 3. Create S3 Bucket for Frontend

1. Navigate to S3 in AWS console
2. Create a new bucket:
   - Set a unique name
   - Enable static website hosting
   - Configure permissions to allow public access

### 4. Set Up CloudFront (Optional but Recommended)

1. Navigate to CloudFront in AWS console
2. Create a distribution:
   - Origin domain: Your S3 bucket website endpoint
   - Redirect HTTP to HTTPS
   - Alternate domain names: your-domain.com, www.your-domain.com
   - SSL certificate: Custom SSL certificate (request one via ACM)
   - Default root object: index.html

## Frontend Deployment

### Using the Deployment Script

1. Edit the `deploy_to_aws.sh` script to set your configuration variables
2. Run the script to build and deploy the frontend:

```bash
chmod +x deploy_to_aws.sh
./deploy_to_aws.sh --deploy-frontend
```

### Manual Deployment

1. Build the frontend assets:

```bash
cd ../frontend
npm install
npm run build
node fix_css.js  # Run CSS optimization
```

2. Upload to S3:

```bash
aws s3 sync build/ s3://your-bucket-name/ --delete
```

3. Invalidate CloudFront cache (if using CloudFront):

```bash
aws cloudfront create-invalidation --distribution-id YOUR_DISTRIBUTION_ID --paths "/*"
```

## Backend Deployment

### Using the Deployment Script

1. Edit the `deploy_to_aws.sh` script to set your configuration variables
2. Run the script to deploy the backend:

```bash
./deploy_to_aws.sh --deploy-backend
```

### Manual Setup on EC2

1. SSH into your EC2 instance:

```bash
ssh -i your-key.pem ec2-user@your-ec2-ip
```

2. Install required software:

```bash
sudo yum update -y
sudo yum install -y python3-pip python3-devel gcc postgresql-devel git
```

3. Install and configure Mosquitto MQTT broker:

```bash
sudo amazon-linux-extras install epel -y
sudo yum install -y mosquitto
sudo systemctl start mosquitto
sudo systemctl enable mosquitto

# Secure MQTT - edit the configuration
sudo nano /etc/mosquitto/mosquitto.conf
```

Add the following configuration:

```
# MQTT Configuration
listener 1883 localhost
listener 8883
allow_anonymous false
password_file /etc/mosquitto/pwfile
certfile /etc/mosquitto/certs/server.crt
keyfile /etc/mosquitto/certs/server.key
```

4. Create MQTT credentials:

```bash
sudo mosquitto_passwd -c /etc/mosquitto/pwfile clearbox_user
# Enter a password when prompted
sudo systemctl restart mosquitto
```

5. Set up the systemd service:

```bash
# Copy the provided clearbox.service to the EC2 instance
sudo cp clearbox.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable clearbox
sudo systemctl start clearbox
```

## Database Migration

### Using the Deployment Script

```bash
./deploy_to_aws.sh --migrate
```

### Manual Migration

1. SSH into your EC2 instance
2. Navigate to the application directory:

```bash
cd ~/clearbox
```

3. Run the migration script:

```bash
python3 -m migrations.migrate_to_postgres
```

## Domain Configuration

1. Create a hosted zone in Route 53 for your domain
2. Create DNS records:
   - A record for @ pointing to CloudFront distribution (for frontend)
   - A record for api pointing to your EC2 instance IP (for backend)
   - CNAME record for www pointing to your main domain

## Monitoring Setup

1. Set up CloudWatch alarms for:
   - EC2 instance CPU/memory usage
   - RDS database metrics
   - API endpoint health checks

2. Configure AWS SNS for notifications

## Maintenance

### Regular Updates

1. Keep the system updated:

```bash
sudo yum update -y
```

2. Update application dependencies:

```bash
cd ~/clearbox
python3 -m pip install --upgrade -r requirements.txt
```

### Database Backups

AWS RDS provides automated backups. Configure the backup window and retention period in the RDS console.

### Security Updates

1. Regularly update security keys:

```bash
./deploy_to_aws.sh --generate-keys
```

Then update the systemd service file and restart:

```bash
sudo nano /etc/systemd/system/clearbox.service
sudo systemctl daemon-reload
sudo systemctl restart clearbox
```

## Troubleshooting

### Backend Issues

- Check service status:

```bash
sudo systemctl status clearbox
```

- View service logs:

```bash
sudo journalctl -u clearbox
```

### Frontend Issues

- Check S3 bucket permissions
- Verify CloudFront distribution settings
- Test the CloudFront URL directly

### Database Issues

- Verify security group allows connections from EC2
- Check the connection string in the service configuration
- Test the connection using psql:

```bash
psql -h your-rds-endpoint -U username -d database_name
``` 