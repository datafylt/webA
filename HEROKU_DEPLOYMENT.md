# Heroku Deployment Guide for Formation Électro API

This guide will help you deploy your FastAPI application to Heroku with PostgreSQL.

## Prerequisites

1. [Heroku CLI](https://devcenter.heroku.com/articles/heroku-cli) installed
2. Git installed
3. A Heroku account

## Step 1: Install Dependencies
~~~~
First, install the PostgreSQL dependencies locally to test:

```bash
cd D:\_datafylt-fastAPI\webA
pip install -r requirements.txt
```

## Step 2: Initialize Git Repository (if not already done)

```bash
cd D:\_datafylt-fastAPI\webA
git init
git add .
git commit -m "Initial commit for Heroku deployment"
```

## Step 3: Create Heroku App

```bash
# Login to Heroku
heroku login

# Create a new Heroku app (replace with your desired name)
heroku create formation-electro-api

# Or if you want Heroku to generate a random name:
heroku create
```

## Step 4: Add PostgreSQL to Your Heroku App

```bash
# Add Heroku Postgres (paid tier - Essential $5/month)
heroku addons:create heroku-postgresql:essential-0

# Verify the DATABASE_URL was set
heroku config:get DATABASE_URL
```

## Step 5: Set Environment Variables

Set all your environment variables on Heroku:

```bash
# SMTP Configuration
heroku config:set SMTP_HOST=smtp.ionos.com
heroku config:set SMTP_PORT=465
heroku config:set SMTP_USER=administration@formationelectro.com
heroku config:set SMTP_PASSWORD="951753!!!Yoric"
heroku config:set SMTP_FROM_EMAIL=administration@formationelectro.com
heroku config:set SMTP_FROM_NAME="Formation Électro"
heroku config:set SMTP_USE_TLS=false
heroku config:set SMTP_USE_SSL=true
heroku config:set EMAIL_TEST_MODE=false

# Application Configuration
heroku config:set SECRET_KEY=3488a63e1765035d386f05409663f55c83bfae3b3c61a932744b20ad14244dcf
heroku config:set DEBUG=false
heroku config:set DB_USE_POSTGRES=true
```

## Step 6: Deploy to Heroku

```bash
# Push your code to Heroku
git push heroku main

# If your main branch is named 'master':
# git push heroku master

# Check the logs
heroku logs --tail
```

The `release` command in Procfile will automatically run database migrations.

## Step 7: Open Your App

```bash
heroku open
```

Your API should now be live! Access it at:
- API: `https://your-app-name.herokuapp.com`
- API Docs: `https://your-app-name.herokuapp.com/docs`

## Useful Heroku Commands

```bash
# View logs
heroku logs --tail

# Open a bash shell on Heroku
heroku run bash

# Check database info
heroku pg:info

# Access PostgreSQL console
heroku pg:psql

# Restart the app
heroku restart

# Check environment variables
heroku config

# Scale dynos
heroku ps:scale web=1

# Run migrations manually (if needed)
heroku run aerich upgrade
```

## Local Testing with PostgreSQL

To test PostgreSQL locally before deploying:

1. Install PostgreSQL on your machine
2. Create a database:
   ```sql
   CREATE DATABASE formation_electro;
   ```
3. Update your `.env` file:
   ```
   DATABASE_URL=postgresql://username:password@localhost:5432/formation_electro
   DB_USE_POSTGRES=true
   ```
4. Run migrations:
   ```bash
   aerich upgrade
   ```
5. Start the server:
   ```bash
   python run.py
   ```

## Switching Back to SQLite for Local Development

Simply update your `.env` file:

```
DATABASE_URL=
DB_USE_POSTGRES=false
```

The application will automatically use SQLite when DATABASE_URL is empty.

## Troubleshooting

### Issue: Migrations not running

```bash
# Manually run migrations
heroku run aerich upgrade
```

### Issue: App won't start

```bash
# Check logs
heroku logs --tail

# Common issues:
# 1. Missing environment variables
# 2. Database connection issues
# 3. Port binding issues
```

### Issue: Database connection errors

```bash
# Check DATABASE_URL is set
heroku config:get DATABASE_URL

# Verify PostgreSQL addon
heroku addons:info heroku-postgresql
```

## Production Checklist

- [ ] All environment variables set on Heroku
- [ ] Database migrations completed
- [ ] SMTP credentials verified
- [ ] SECRET_KEY is different from default
- [ ] DEBUG=false in production
- [ ] API documentation accessible at /docs
- [ ] Test email sending functionality
- [ ] Monitor application logs

## Cost Considerations

- **Heroku Dyno**: Basic ($7/month) or Eco ($5/month)
- **Heroku PostgreSQL**: Essential-0 ($5/month) - 10M rows, 20 connections
- Total minimum: ~$10-12/month

## Support

For issues:
- Check logs: `heroku logs --tail`
- Heroku docs: https://devcenter.heroku.com/
