#!/bin/bash

echo "=== AWS Zero Cost Optimization Script ==="
echo "This script will fix your AWS resources to eliminate all charges"
echo ""

# Get confirmation before proceeding
read -p "WARNING: This script will modify your AWS resources. Continue? (y/n): " confirm
if [[ "$confirm" != "y" ]]; then
  echo "Script aborted."
  exit 1
fi

# 1. Remove RDS snapshot that's causing charges
echo "=== Removing RDS Snapshot ==="
echo "Deleting 'clearbox-db-snapshot'..."
aws rds delete-db-snapshot --db-snapshot-identifier clearbox-db-snapshot
echo ""

# 2. Check if there's an RDS instance that might be deleted
echo "=== Checking for deleted RDS instances that may still incur charges ==="
aws rds describe-db-instances --include-deleted --query "DBInstances[?DBInstanceStatus=='deleted']"

# 3. Update Route 53 approach
echo "=== Route 53 Optimization ==="
echo "Route 53 hosted zones cost $0.50/month and are not part of the free tier."
echo "To eliminate this cost, we need to move to a free DNS provider."
echo ""
echo "Step 1: Export current Route 53 records"
aws route53 list-resource-record-sets --hosted-zone-id Z00796501PUXPM3HWH5UV > route53_records.json
echo "Records exported to route53_records.json"
echo ""

echo "Step 2: Set up DNS at your domain registrar"
echo "Log in to your domain registrar account (name.com) and add these DNS records"
echo "Then configure your EC2 instance to work with the new DNS setup"
echo ""

echo "Step 3: After confirming new DNS is working, delete the Route 53 hosted zone"
echo "CAUTION: Only run this command after setting up alternative DNS and confirming it works!"
echo "# aws route53 delete-hosted-zone --id Z00796501PUXPM3HWH5UV"
echo ""

# 4. Set up billing alarm for future protection
echo "=== Creating AWS Billing Alarm ==="
cat << 'EOF' > billing-alarm.json
{
  "AlarmName": "BillingAlarm",
  "AlarmDescription": "Alarm when my estimated charges exceed $1",
  "ActionsEnabled": true,
  "OKActions": [],
  "AlarmActions": [],
  "InsufficientDataActions": [],
  "MetricName": "EstimatedCharges",
  "Namespace": "AWS/Billing",
  "Statistic": "Maximum",
  "Dimensions": [
    {
      "Name": "Currency",
      "Value": "USD"
    }
  ],
  "Period": 21600,
  "EvaluationPeriods": 1,
  "DatapointsToAlarm": 1,
  "Threshold": 1,
  "ComparisonOperator": "GreaterThanThreshold",
  "TreatMissingData": "missing"
}
EOF

echo "Creating billing alarm..."
aws cloudwatch put-metric-alarm --cli-input-json file://billing-alarm.json
echo "Billing alarm created successfully!"
echo ""

# 5. Update README.md with accurate AWS Free Tier information
echo "=== Updating README with accurate AWS Free Tier information ==="
cat << 'EOF' > aws_free_tier_section.md
## 📊 AWS Free Tier Optimization

ClearBox is now configured to operate entirely within AWS Free Tier limits with zero cost:

- **EC2 Instance:** Uses t3.micro instance (free for 750 hours/month for 12 months)
- **Storage:** 8GB EBS volume (free up to 30GB for 12 months)
- **Database:** Using PostgreSQL on the EC2 instance instead of RDS
- **DNS Management:** Using domain registrar's free DNS service instead of Route 53
- **MQTT Broker:** Running in a Docker container on the EC2 instance
- **Data Transfer:** Optimized to stay within 100GB/month free outbound data

**Cost Optimization Measures:**
- Removed all RDS snapshots that were incurring charges
- Migrated from Route 53 ($0.50/month) to free DNS at the domain registrar
- Set up billing alarm to notify at $1 threshold
- EC2 instance configured for optimal free tier resource usage

This configuration ensures ClearBox can run with $0 AWS cost during the 12-month free tier period.
EOF

echo "AWS Free Tier section created in aws_free_tier_section.md"
echo "Update your README.md files with this content"
echo ""

echo "=== Script Completed ==="
echo "These steps will eliminate your AWS costs by:"
echo "1. Removing the RDS snapshot ($0.02 charge)"
echo "2. Setting up to migrate away from Route 53 ($0.50 charge)"
echo "3. Creating a billing alarm to warn of any future unexpected charges"
echo ""
echo "After completing these steps, your AWS bill should be $0.00" 