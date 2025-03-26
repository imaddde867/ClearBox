# ClearBox AWS Deployment Checklist

Use this checklist to ensure you've completed all necessary steps for deploying ClearBox to AWS free tier.

## Pre-Deployment Preparation

- [ ] Generate new secure keys for production environment
  ```bash
  cd scripts
  ./generate_keys.py --env-file ../backend/.env.template
  ```

- [ ] Check dependencies for security vulnerabilities
  ```bash
  cd scripts
  ./check_dependencies.py --report security_report.md
  ```

- [ ] Update frontend API configuration with production URLs in `src/config.js`

- [ ] Build production frontend assets
  ```bash
  cd frontend
  npm run build:production
  ```

- [ ] Configure `.env` file from `.env.template` with production values
  - [ ] Set PostgreSQL connection string for RDS
  - [ ] Set secure JWT and encryption keys
  - [ ] Configure MQTT settings
  - [ ] Update CORS settings with your domain

## AWS Infrastructure Setup

- [ ] Launch EC2 instance (t2.micro)
  - [ ] Configure security groups
  - [ ] Set up SSH key pair

- [ ] Create RDS PostgreSQL instance (db.t2.micro)
  - [ ] Configure security groups to allow EC2 access
  - [ ] Set strong password
  - [ ] Configure automated backups

- [ ] Create S3 bucket for frontend assets
  - [ ] Enable static website hosting
  - [ ] Configure public access

- [ ] Request SSL certificates from AWS Certificate Manager
  - [ ] Domain validation
  - [ ] For both main domain and API subdomain

- [ ] Set up CloudFront distribution (optional)
  - [ ] Point to S3 bucket origin
  - [ ] Configure SSL certificate
  - [ ] Configure cache behaviors

- [ ] Create Route 53 hosted zone (if using your own domain)
  - [ ] Set up A records for frontend and API

## Backend Deployment

- [ ] Upload backend code to EC2
  ```bash
  cd deploy
  ./deploy_to_aws.sh --deploy-backend
  ```

- [ ] Set up systemd service
  ```bash
  # On EC2 instance
  sudo cp clearbox.service /etc/systemd/system/
  sudo systemctl daemon-reload
  sudo systemctl enable clearbox
  sudo systemctl start clearbox
  ```

- [ ] Configure Nginx
  ```bash
  # On EC2 instance
  sudo cp nginx/clearbox.conf /etc/nginx/conf.d/
  sudo nginx -t
  sudo systemctl restart nginx
  ```

- [ ] Install and configure Mosquitto MQTT
  ```bash
  # On EC2 instance
  sudo systemctl start mosquitto
  sudo systemctl enable mosquitto
  ```

## Database Migration

- [ ] Run database migration
  ```bash
  cd deploy
  ./deploy_to_aws.sh --migrate
  ```

- [ ] Verify database tables and data

## Frontend Deployment

- [ ] Deploy frontend to S3
  ```bash
  cd deploy
  ./deploy_to_aws.sh --deploy-frontend
  ```

- [ ] Invalidate CloudFront cache (if using CloudFront)

## Post-Deployment Verification

- [ ] Check backend API status
  ```bash
  curl https://api.your-domain.com/api
  ```

- [ ] Test frontend loading
  - [ ] Open https://your-domain.com in browser
  - [ ] Verify assets load correctly

- [ ] Test user signup and login
  - [ ] Create a test account
  - [ ] Verify login works

- [ ] Test messaging functionality
  - [ ] Send and receive messages
  - [ ] Verify encryption works

- [ ] Verify MQTT connections
  - [ ] Check for successful WebSocket connections
  - [ ] Verify real-time messaging

## Monitoring Setup

- [ ] Set up CloudWatch Alarms
  - [ ] EC2 CPU utilization
  - [ ] RDS metrics
  - [ ] API health checks

- [ ] Configure logging
  - [ ] EC2 instance logs
  - [ ] RDS logs
  - [ ] S3 access logs

- [ ] Set up billing alerts
  - [ ] Configure to stay within free tier limits

## Security Final Check

- [ ] Verify HTTPS is enforced
- [ ] Confirm SSL certificate is valid
- [ ] Check security headers are set correctly
- [ ] Test for sensitive information exposure
- [ ] Verify proper authentication is required for all API endpoints
- [ ] Confirm database is properly secured

## Documentation

- [ ] Update README with production URLs
- [ ] Document deployment process
- [ ] Update API documentation

## Final Steps

- [ ] Create EC2 instance AMI for backup
- [ ] Take manual RDS snapshot
- [ ] Document rollback procedures 