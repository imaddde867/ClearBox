#!/bin/bash
# ClearBox AWS Deployment Script
# This script helps deploy the ClearBox application to AWS

set -e

# Color codes for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Configuration variables - Edit these for your environment
EC2_INSTANCE_IP=""
EC2_PEM_FILE=""
RDS_ENDPOINT=""
S3_BUCKET_NAME=""
DOMAIN_NAME=""
CLOUDFRONT_DISTRIBUTION_ID=""

# Function to display usage
usage() {
    echo -e "${YELLOW}ClearBox AWS Deployment Script${NC}"
    echo -e "Usage: $0 [options]"
    echo
    echo -e "Options:"
    echo -e "  --setup            Setup initial AWS resources"
    echo -e "  --deploy-frontend  Build and deploy frontend"
    echo -e "  --deploy-backend   Deploy backend"
    echo -e "  --deploy-all       Deploy both frontend and backend"
    echo -e "  --migrate          Run database migration"
    echo -e "  --generate-keys    Generate new secure keys"
    echo -e "  --help             Display this help message"
    echo
    echo -e "Examples:"
    echo -e "  $0 --setup"
    echo -e "  $0 --deploy-all"
    echo
    exit 0
}

# Function to check if AWS CLI is installed
check_aws_cli() {
    if ! command -v aws &> /dev/null; then
        echo -e "${RED}Error: AWS CLI is not installed. Please install it first.${NC}"
        echo "Visit: https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html"
        exit 1
    fi
}

# Function to check if AWS CLI is configured
check_aws_config() {
    if ! aws sts get-caller-identity &> /dev/null; then
        echo -e "${RED}Error: AWS CLI is not configured. Please run 'aws configure' first.${NC}"
        exit 1
    fi
}

# Function to verify configuration
verify_config() {
    local missing=false
    
    if [ -z "$EC2_INSTANCE_IP" ]; then
        echo -e "${RED}Error: EC2_INSTANCE_IP is not set${NC}"
        missing=true
    fi
    
    if [ -z "$EC2_PEM_FILE" ]; then
        echo -e "${RED}Error: EC2_PEM_FILE is not set${NC}"
        missing=true
    fi
    
    if [ "$missing" = true ]; then
        echo -e "${YELLOW}Please edit this script to set all required configuration variables.${NC}"
        exit 1
    fi
}

# Function to set up AWS resources
setup_aws_resources() {
    echo -e "${GREEN}Setting up AWS resources...${NC}"
    
    # 1. Create S3 bucket for frontend
    echo -e "${YELLOW}Creating S3 bucket...${NC}"
    if aws s3 ls "s3://$S3_BUCKET_NAME" 2>&1 | grep -q 'NoSuchBucket'; then
        aws s3 mb "s3://$S3_BUCKET_NAME" --region us-east-1
        aws s3 website "s3://$S3_BUCKET_NAME" --index-document index.html --error-document index.html
        echo -e "${GREEN}S3 bucket created successfully.${NC}"
    else
        echo -e "${YELLOW}S3 bucket already exists.${NC}"
    fi
    
    # 2. Set up S3 bucket policy for public access
    echo -e "${YELLOW}Setting up S3 bucket policy...${NC}"
    cat > /tmp/bucket-policy.json << EOF
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "PublicReadGetObject",
            "Effect": "Allow",
            "Principal": "*",
            "Action": "s3:GetObject",
            "Resource": "arn:aws:s3:::$S3_BUCKET_NAME/*"
        }
    ]
}
EOF
    aws s3api put-bucket-policy --bucket "$S3_BUCKET_NAME" --policy file:///tmp/bucket-policy.json
    
    # 3. Instructions for remaining setup
    echo
    echo -e "${GREEN}Basic AWS setup complete.${NC}"
    echo
    echo -e "${YELLOW}Next steps:${NC}"
    echo -e "1. Create an EC2 instance using the AWS console or CLI."
    echo -e "2. Create an RDS PostgreSQL instance."
    echo -e "3. Configure security groups to allow traffic between EC2 and RDS."
    echo -e "4. Request an SSL certificate from AWS Certificate Manager."
    echo -e "5. Set up CloudFront distribution pointing to the S3 bucket."
    echo -e "6. Update Route53 to point your domain to CloudFront and EC2."
    echo
    echo -e "Once you've completed these steps, update the configuration variables in this script."
    echo
}

# Function to generate secure keys for production
generate_keys() {
    echo -e "${GREEN}Generating new secure keys for production...${NC}"
    
    # Generate JWT secret key
    JWT_SECRET=$(openssl rand -hex 32)
    
    # Generate encryption key
    ENCRYPTION_KEY=$(openssl rand -hex 32)
    
    echo -e "${GREEN}Keys generated successfully.${NC}"
    echo
    echo -e "JWT Secret Key: ${YELLOW}$JWT_SECRET${NC}"
    echo -e "Encryption Key: ${YELLOW}$ENCRYPTION_KEY${NC}"
    echo
    echo -e "${YELLOW}Make sure to update these keys in your production .env file${NC}"
}

# Function to build and optimize the frontend
build_frontend() {
    echo -e "${GREEN}Building and optimizing frontend...${NC}"
    
    # Navigate to frontend directory
    cd ../frontend
    
    # Install dependencies
    echo -e "${YELLOW}Installing frontend dependencies...${NC}"
    npm install
    
    # Build the production assets
    echo -e "${YELLOW}Building frontend assets...${NC}"
    npm run build
    
    # Optimize assets
    echo -e "${YELLOW}Optimizing frontend assets...${NC}"
    
    # Install compression tools if not already installed
    if ! command -v npx &> /dev/null; then
        npm install -g npx
    fi
    
    # Install compression packages if needed
    if ! [ -d "node_modules/gzip-size" ]; then
        npm install --save-dev gzip-size
    fi
    
    # Run custom optimization script
    echo -e "${YELLOW}Running CSS optimization...${NC}"
    node fix_css.js
    
    echo -e "${GREEN}Frontend build and optimization complete.${NC}"
    
    # Return to original directory
    cd -
}

# Function to deploy frontend to S3
deploy_frontend() {
    echo -e "${GREEN}Deploying frontend to S3...${NC}"
    
    # First build the frontend
    build_frontend
    
    # Deploy to S3
    echo -e "${YELLOW}Uploading to S3 bucket...${NC}"
    aws s3 sync ../frontend/build/ "s3://$S3_BUCKET_NAME/" --delete
    
    # Invalidate CloudFront cache if distribution ID is provided
    if [ -n "$CLOUDFRONT_DISTRIBUTION_ID" ]; then
        echo -e "${YELLOW}Invalidating CloudFront cache...${NC}"
        aws cloudfront create-invalidation --distribution-id "$CLOUDFRONT_DISTRIBUTION_ID" --paths "/*"
    fi
    
    echo -e "${GREEN}Frontend deployment complete.${NC}"
    echo -e "Frontend should be available at: ${YELLOW}https://$DOMAIN_NAME${NC}"
}

# Function to deploy backend to EC2
deploy_backend() {
    echo -e "${GREEN}Deploying backend to EC2...${NC}"
    
    # Verify SSH key file exists
    if [ ! -f "$EC2_PEM_FILE" ]; then
        echo -e "${RED}Error: EC2 PEM file not found: $EC2_PEM_FILE${NC}"
        exit 1
    fi
    
    # Create a temporary deployment folder
    DEPLOY_TMP=$(mktemp -d)
    
    # Copy backend files to temporary folder
    echo -e "${YELLOW}Preparing backend files...${NC}"
    cp -r ../backend/* "$DEPLOY_TMP/"
    
    # Create a deployment package
    DEPLOY_PACKAGE="clearbox_backend_$(date +%Y%m%d_%H%M%S).tar.gz"
    tar -czf "$DEPLOY_PACKAGE" -C "$DEPLOY_TMP" .
    
    # Upload to EC2
    echo -e "${YELLOW}Uploading to EC2 instance...${NC}"
    scp -i "$EC2_PEM_FILE" "$DEPLOY_PACKAGE" "ec2-user@$EC2_INSTANCE_IP:~/"
    
    # Deploy on EC2
    echo -e "${YELLOW}Deploying on EC2 instance...${NC}"
    ssh -i "$EC2_PEM_FILE" "ec2-user@$EC2_INSTANCE_IP" << EOF
        # Extract files
        mkdir -p ~/clearbox
        tar -xzf ~/$DEPLOY_PACKAGE -C ~/clearbox
        
        # Install or update dependencies
        cd ~/clearbox
        python3 -m pip install --upgrade -r requirements.txt
        
        # Restart the service
        sudo systemctl restart clearbox
        
        # Clean up
        rm ~/$DEPLOY_PACKAGE
EOF
    
    # Clean up local temporary files
    rm -f "$DEPLOY_PACKAGE"
    rm -rf "$DEPLOY_TMP"
    
    echo -e "${GREEN}Backend deployment complete.${NC}"
}

# Function to run database migration
run_migration() {
    echo -e "${GREEN}Running database migration...${NC}"
    
    # Verify SSH key file exists
    if [ ! -f "$EC2_PEM_FILE" ]; then
        echo -e "${RED}Error: EC2 PEM file not found: $EC2_PEM_FILE${NC}"
        exit 1
    fi
    
    # Run migration script on EC2
    echo -e "${YELLOW}Executing migration on EC2 instance...${NC}"
    ssh -i "$EC2_PEM_FILE" "ec2-user@$EC2_INSTANCE_IP" << EOF
        cd ~/clearbox
        python3 -m migrations.migrate_to_postgres
EOF
    
    echo -e "${GREEN}Database migration completed.${NC}"
}

# Main script logic
main() {
    # Check for arguments
    if [ $# -eq 0 ]; then
        usage
    fi
    
    # Check AWS CLI is installed and configured
    check_aws_cli
    check_aws_config
    
    # Process arguments
    while [ $# -gt 0 ]; do
        case "$1" in
            --setup)
                setup_aws_resources
                ;;
            --deploy-frontend)
                verify_config
                deploy_frontend
                ;;
            --deploy-backend)
                verify_config
                deploy_backend
                ;;
            --deploy-all)
                verify_config
                deploy_frontend
                deploy_backend
                ;;
            --migrate)
                verify_config
                run_migration
                ;;
            --generate-keys)
                generate_keys
                ;;
            --help)
                usage
                ;;
            *)
                echo -e "${RED}Unknown option: $1${NC}"
                usage
                ;;
        esac
        shift
    done
}

# Run the main function
main "$@" 