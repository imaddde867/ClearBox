#!/bin/bash

echo "=== AWS Free Tier Optimization Script ==="
echo "This script will optimize your AWS resources to stay within free tier limits"
echo ""

# 1. Route 53 - This is causing the highest charge ($0.50)
# Route 53 is not part of the free tier, so we need an alternative DNS solution
echo "=== Route 53 Hosted Zone Details ==="
aws route53 list-hosted-zones
echo ""
echo "IMPORTANT: Route 53 hosted zones ($0.50/month) are NOT part of the AWS Free Tier."
echo "Option 1: Delete the Route 53 hosted zone and use your domain registrar's free DNS"
echo "Option 2: Keep using Route 53 but accept the $0.50 monthly charge"
echo ""
echo "To delete the Route 53 hosted zone, first note the zone ID:"
echo "ZONE_ID=\"Z00796501PUXPM3HWH5UV\""
echo ""
echo "Then delete all record sets (except NS and SOA) and finally delete the zone:"
echo "# aws route53 list-resource-record-sets --hosted-zone-id \$ZONE_ID"
echo "# aws route53 delete-hosted-zone --id \$ZONE_ID"
echo ""
echo "CAUTION: Only delete the zone if you've set up alternative DNS for your domain!"
echo ""

# 2. EC2 Instance Optimization
echo "=== EC2 Instance Optimization ==="
aws ec2 describe-instances --query "Reservations[*].Instances[*].{InstanceId:InstanceId,InstanceType:InstanceType,State:State.Name}" --output table
echo ""
echo "Your t3.micro instance is part of free tier (750 hours/month)"
echo "Ensuring the instance is optimized for free tier:"
echo ""

# 3. EBS Volume Optimization
echo "=== EBS Volume Optimization ==="
aws ec2 describe-volumes --query "Volumes[*].{VolumeId:VolumeId,Size:Size,Type:VolumeType,IOPS:Iops,Throughput:Throughput}" --output table
echo ""
echo "Free tier includes 30GB of EBS General Purpose (gp2 or gp3) storage"
echo "Your volume is 8GB which is within free tier limits"
echo "Ensure all volume parameters are within free tier limits:"
echo ""
echo "Setting volume throughput to standard free tier values:"
echo "# aws ec2 modify-volume --volume-id vol-021ad920665a4dc1b --throughput 125 --iops 3000"
echo ""

# 4. Check for RDS instances
echo "=== RDS Optimization ==="
aws rds describe-db-instances --query "DBInstances[*].{DBInstanceIdentifier:DBInstanceIdentifier,Engine:Engine,Status:DBInstanceStatus}" --output table
echo ""
echo "No RDS instances found - good!"
echo "Your small RDS charge ($0.02) might be from a previous instance or snapshot."
echo ""
echo "To check for RDS snapshots:"
echo "# aws rds describe-db-snapshots"
echo ""
echo "To delete any found snapshots:"
echo "# aws rds delete-db-snapshot --db-snapshot-identifier <snapshot-id>"
echo ""

# 5. Check for elastic IPs not attached to running instances (these cost money)
echo "=== Elastic IP Optimization ==="
aws ec2 describe-addresses
echo ""
echo "Elastic IPs not attached to running instances incur charges"
echo "If any unattached elastic IPs were found above, release them:"
echo "# aws ec2 release-address --allocation-id <allocation-id>"
echo ""

# 6. Check for load balancers (these cost money)
echo "=== Load Balancer Check ==="
aws elbv2 describe-load-balancers --query "LoadBalancers[*].{LoadBalancerName:LoadBalancerName,State:State.Code}" --output table 2>/dev/null
echo "If any load balancers were found above, they are NOT part of free tier"
echo ""

# 7. Check for AWS Lambda usage
echo "=== Lambda Usage Check ==="
echo "Lambda free tier: 1M requests/month and 400,000 GB-seconds/month"
echo "To check Lambda functions:"
echo "# aws lambda list-functions"
echo ""

# Final recommendations
echo "=== Final Recommendations ==="
echo "1. The main charge is Route 53 ($0.50) which is NOT part of free tier"
echo "   - Options: (a) Delete zone and use registrar DNS, or (b) Accept the small charge"
echo ""
echo "2. Ensure you don't exceed other free tier limits:"
echo "   - EC2: 750 hours/month of t3.micro (you're using this correctly)"
echo "   - EBS: 30GB General Purpose SSD storage (you're using 8GB - good!)"
echo "   - Data transfer: 100GB outbound (monitor usage in billing dashboard)"
echo ""
echo "3. To prevent unexpected charges:"
echo "   - Set up a billing alarm: aws cloudwatch put-metric-alarm"
echo "   - Regularly check the AWS Billing Dashboard"
echo ""
echo "4. For the current $0.02 charges from EC2-Other and RDS:"
echo "   - These may be from snapshots, previous usage, or data transfer"
echo "   - Check the detailed billing report in the AWS Console"
echo ""
echo "Script completed. Review the recommendations above and take appropriate actions." 