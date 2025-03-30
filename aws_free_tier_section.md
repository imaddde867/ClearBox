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
