# ClearBox Deployment Guide

This document outlines the steps to deploy ClearBox to a production environment using entirely free services:
- Frontend: Netlify (static hosting)
- Backend: Render (web service)
- Database: Supabase (PostgreSQL)
- MQTT Broker: HiveMQ Cloud (free tier)
- Domain: clearbox.live

## Prerequisites

- GitHub account
- Netlify account
- Render account
- Supabase account
- HiveMQ Cloud account
- Domain (clearbox.live) with ability to manage DNS records

## Step 1: Database Setup with Supabase

1. Sign up at [supabase.com](https://supabase.com/) (free tier)
2. Create a new project named "clearbox"
3. In the SQL Editor, create your database tables using the SQL provided in the repository
4. Get your connection string from Settings → Database → Connection string (select "URI")
5. Save this connection string for the backend deployment
   - Database URL: `postgresql://postgres:120705imad@db.nnitebsysgmcdhelglqx.supabase.co:5432/postgres`

## Step 2: MQTT Broker Setup with HiveMQ Cloud

1. Sign up at [HiveMQ Cloud](https://www.hivemq.com/cloud/) (free plan)
2. Create a new cluster (the free tier allows 100 concurrent connections)
3. Create credentials by adding a new user
4. Note the following details:
   - Broker URL: `beb6c3d91a0e4befbb836d5269d627ea.s1.eu.hivemq.cloud`
   - Port: `8883` for secure MQTT
   - WebSocket Port: `8884` for secure WebSockets
   - Username: `imadeddine200507`
   - Password: `120705Imad`

## Step 3: Backend Deployment to Render

### Option 1: Deploy with render.yaml (Recommended)

1. Ensure your repository contains the `render.yaml` file
2. Connect to Render and create a new Blueprint instance
3. Select your GitHub repository
4. Configure the secret environment variables in the Render dashboard:
   - `DATABASE_URL`: `postgresql://postgres:120705imad@db.nnitebsysgmcdhelglqx.supabase.co:5432/postgres`
   - `SECRET_KEY`: (generate a strong random string)
   - `MQTT_BROKER`: `beb6c3d91a0e4befbb836d5269d627ea.s1.eu.hivemq.cloud`
   - `MQTT_PORT`: `8883`
   - `MQTT_USERNAME`: `imadeddine200507`
   - `MQTT_PASSWORD`: `120705Imad`
   - `MQTT_USE_SSL`: `true`
   - `ENCRYPTION_KEY`: (generate a strong random string)
   - `CORS_ORIGINS`: `https://clearbox.live`

### Option 2: Manual Deployment

1. Sign up at [render.com](https://render.com/) (free tier)
2. Click "New Web Service"
3. Connect your GitHub repository
4. Configure the web service:
   - Name: clearbox-api
   - Environment: Python 3.8+
   - Build Command: `pip install -r backend/requirements.txt`
   - Start Command: `cd backend && gunicorn app.main:app --workers 4 --worker-class uvicorn.workers.UvicornWorker`
   - Select "Free" plan
5. Add the environment variables as listed above

## Step 4: Frontend Deployment to Netlify

### Option 1: Deploy with netlify.toml (Recommended)

1. Ensure your repository contains the `netlify.toml` file
2. Connect to Netlify and create a new site from Git
3. Select your GitHub repository
4. Configure the build settings if needed
5. Add the following environment variables in the Netlify dashboard:
   - `REACT_APP_API_URL=https://clearbox-api.onrender.com` (your Render backend URL)
   - `REACT_APP_MQTT_URL=wss://beb6c3d91a0e4befbb836d5269d627ea.s1.eu.hivemq.cloud:8884/mqtt`
   - `REACT_APP_MQTT_USERNAME=imadeddine200507`
   - `REACT_APP_MQTT_PASSWORD=120705Imad`

### Option 2: Manual Deployment

1. Sign up at [netlify.com](https://netlify.com/) (free tier)
2. Click "New site from Git"
3. Connect to your GitHub repository
4. Configure the build settings:
   - Base directory: `frontend`
   - Build command: `npm run build`
   - Publish directory: `build`
5. Add the environment variables as listed above
6. Click "Deploy site"

## Step 5: Domain Configuration (clearbox.live)

1. In your domain registrar's DNS settings, add the following records:
   - Point `clearbox.live` to your Netlify site using an ANAME/ALIAS record (or CNAME if ANAME not supported)
   - Add CNAME record `api.clearbox.live` pointing to your Render backend URL
2. In Netlify, go to Domain settings and add your custom domain
3. In Render, go to your web service settings and add your custom subdomain (`api.clearbox.live`)

## Step 6: Verify Deployment

1. Visit your site at `https://clearbox.live`
2. Test login, registration, and messaging features
3. Check that backend is accessible at `https://api.clearbox.live/api`
4. Verify MQTT connections are working by checking browser console logs
5. Monitor logs in Netlify and Render for any errors

## MQTT Testing

To test your MQTT connection:

1. Open the browser console on your deployed site
2. Log in to your application
3. Look for logs like "MQTT client connected" and "Subscribed to user/{userId}/messages"
4. Send messages between two browsers/users and verify they're delivered via MQTT
5. If messages are not being delivered, check:
   - MQTT credential configuration in the frontend
   - Network connectivity to HiveMQ (check browser network tab)
   - Any errors in the browser console

## Troubleshooting

- **CORS errors**: Check the CORS_ORIGINS environment variable in your backend
- **Database connection issues**: Verify the DATABASE_URL is correct and that the IP is whitelisted in Supabase
- **MQTT connection problems**: Check that the MQTT credentials and URL are correct
  - Confirm WebSocket connection port 8884 is used for browser connections
  - Verify SSL is enabled for the connection
  - Try connecting with an MQTT test client to isolate issues
- **API endpoints not found**: Ensure the REACT_APP_API_URL is set correctly in frontend environment variables

## Scaling Beyond Free Tier

When your application grows:
1. Upgrade to paid Supabase plan for more storage and connections
2. Upgrade to paid Render plan for better performance and uptime
3. Consider using a dedicated MQTT broker or paid HiveMQ plan
4. Set up a CDN for your frontend assets

## Security Recommendations

1. Regularly rotate secrets and API keys
2. Enable two-factor authentication on all services
3. Set up automated security scanning of your codebase
4. Configure proper Content Security Policy in your Netlify configuration
5. For production use, replace hardcoded MQTT credentials with proper environment variables 