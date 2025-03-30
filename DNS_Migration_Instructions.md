# DNS Migration Instructions for ClearBox.live

## Why Migrate DNS?

Route 53 is costing $0.50/month and is not part of the AWS Free Tier. By migrating to your domain registrar's free DNS service (name.com), you can eliminate this charge completely.

## Records to Migrate

Based on your Route 53 configuration, you need to set up the following DNS records at name.com:

1. **A Record for clearbox.live**
   - Name: @ (or blank, representing the root domain)
   - Value: 51.21.169.163
   - TTL: 300 seconds (or 5 minutes)

2. **A Record for www.clearbox.live**
   - Name: www
   - Value: 51.21.169.163
   - TTL: 300 seconds (or 5 minutes)

## Migration Steps

1. **Log in to name.com**
   - Sign in to your name.com account where clearbox.live is registered

2. **Access DNS Settings**
   - Find the domain clearbox.live in your account
   - Go to "Manage DNS" or "DNS Records" section

3. **Add the A Records**
   - Add the root A record pointing to 51.21.169.163
   - Add the www A record pointing to 51.21.169.163
   - Save the changes

4. **Update Nameservers (if needed)**
   - If you're currently using Route 53 nameservers, you'll need to change them back to name.com's nameservers
   - This step is only necessary if you previously changed the nameservers to Route 53

5. **Wait for DNS Propagation**
   - DNS changes can take up to 48 hours to fully propagate, but often complete within a few hours
   - You can use tools like https://dnschecker.org to monitor propagation

6. **Test the Website**
   - Once DNS has propagated, verify that https://clearbox.live and https://www.clearbox.live are working properly

7. **Delete Route 53 Hosted Zone**
   - Only after confirming the site is fully functional with the new DNS, run:
   ```bash
   aws route53 delete-hosted-zone --id Z00796501PUXPM3HWH5UV
   ```

## Verifying Successful Migration

1. **Website Check**
   - Both https://clearbox.live and https://www.clearbox.live should load correctly

2. **DNS Lookup**
   - Run `dig clearbox.live` or use an online DNS lookup tool
   - Verify it's now resolving through name.com nameservers, not Route 53

3. **AWS Billing**
   - Check your AWS Billing dashboard in a few days to confirm Route 53 charges have stopped

## Additional Considerations

- **SSL Certificate**: Ensure your Let's Encrypt certificate continues to renew correctly
- **Backup DNS Configuration**: Keep a copy of this DNS configuration for future reference
- **Regular Monitoring**: Check your website periodically to ensure DNS remains properly configured

By completing this migration, you'll eliminate the $0.50/month Route 53 charge, making your AWS usage completely free tier compliant with zero cost. 