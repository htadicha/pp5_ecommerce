# 🚀 Deployment Guide - Hawashmart E-Commerce Platform

This guide provides step-by-step instructions for deploying the Hawashmart e-commerce platform to production.

## 📋 Table of Contents

- [Pre-Deployment Checklist](#pre-deployment-checklist)
- [Environment Variables Configuration](#environment-variables-configuration)
- [Heroku Deployment](#heroku-deployment)
- [AWS S3 Configuration (Optional)](#aws-s3-configuration-optional)
- [Post-Deployment Tasks](#post-deployment-tasks)
- [Troubleshooting](#troubleshooting)

---

## ✅ Pre-Deployment Checklist

Before deploying to production, ensure you have completed the following:

- [ ] Generated a strong SECRET_KEY for production
- [ ] Set `DEBUG=False` in production environment
- [ ] Configured all required environment variables
- [ ] Set up PostgreSQL database (Heroku provides this automatically)
- [ ] Collected static files
- [ ] Run all database migrations
- [ ] Configured payment gateway (Stripe)
- [ ] Set up error monitoring (optional but recommended)

---

## 🔐 Environment Variables Configuration

### Required Environment Variables

Create a `.env` file for local development (already in `.gitignore`). For production, set these as environment variables in your hosting platform.

#### 1. Django Settings

```bash
# Generate a strong SECRET_KEY using:
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"

SECRET_KEY='your-generated-secret-key-here'
DEBUG=False
ALLOWED_HOSTS=your-domain.com,www.your-domain.com
```

**⚠️ SECURITY WARNING**: 
- NEVER commit your production SECRET_KEY to version control
- Use a different SECRET_KEY for development and production
- Keep DEBUG=False in production

#### 2. Database Configuration

```bash
# For Heroku: This is automatically provided by Heroku Postgres addon
# For other platforms: Use your PostgreSQL connection string
DATABASE_URL=postgres://user:password@host:port/database
```

#### 3. Stripe Payment Configuration

```bash
# Get these from https://dashboard.stripe.com/apikeys
# For production, use LIVE keys (not test keys)
STRIPE_PUBLIC_KEY='pk_live_xxxxxxxxxxxxx'
STRIPE_SECRET_KEY='sk_live_xxxxxxxxxxxxx'
```

#### 4. AWS S3 Configuration (Optional)

If you want to serve static and media files from AWS S3:

```bash
USE_AWS=True
AWS_ACCESS_KEY_ID=your_aws_access_key_id
AWS_SECRET_ACCESS_KEY=your_aws_secret_access_key
AWS_STORAGE_BUCKET_NAME=your_bucket_name
AWS_S3_REGION_NAME=us-east-1
```

#### 5. Email Configuration (Optional)

For sending transactional emails:

```bash
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your_email@gmail.com
EMAIL_HOST_PASSWORD=your_app_password
```

---

## 🌐 Heroku Deployment

### Prerequisites

1. Install Heroku CLI:
   ```bash
   brew tap heroku/brew && brew install heroku
   # Or download from https://devcenter.heroku.com/articles/heroku-cli
   ```

2. Login to Heroku:
   ```bash
   heroku login
   ```

### Step 1: Create Heroku App

```bash
# Create a new Heroku app
heroku create your-app-name

# Or if you already have an app
heroku git:remote -a your-app-name
```

### Step 2: Add PostgreSQL Database

```bash
# Add Heroku Postgres addon (free tier)
heroku addons:create heroku-postgresql:essential-0

# Verify database was added
heroku config:get DATABASE_URL
```

### Step 3: Set Environment Variables

Set all required environment variables on Heroku:

```bash
# Generate a new SECRET_KEY
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"

# Set environment variables
heroku config:set SECRET_KEY='your-generated-secret-key'
heroku config:set DEBUG=False
heroku config:set ALLOWED_HOSTS='your-app-name.herokuapp.com'

# Stripe keys (use LIVE keys for production)
heroku config:set STRIPE_PUBLIC_KEY='pk_live_xxxxxxxxxxxxx'
heroku config:set STRIPE_SECRET_KEY='sk_live_xxxxxxxxxxxxx'

# AWS S3 (if using)
heroku config:set USE_AWS=True
heroku config:set AWS_ACCESS_KEY_ID='your_aws_access_key'
heroku config:set AWS_SECRET_ACCESS_KEY='your_aws_secret_key'
heroku config:set AWS_STORAGE_BUCKET_NAME='your_bucket_name'
heroku config:set AWS_S3_REGION_NAME='us-east-1'

# Email configuration (if using)
heroku config:set EMAIL_BACKEND='django.core.mail.backends.smtp.EmailBackend'
heroku config:set EMAIL_HOST='smtp.gmail.com'
heroku config:set EMAIL_PORT=587
heroku config:set EMAIL_USE_TLS=True
heroku config:set EMAIL_HOST_USER='your_email@gmail.com'
heroku config:set EMAIL_HOST_PASSWORD='your_app_password'
```

### Step 4: Deploy to Heroku

```bash
# Add changes to git
git add .
git commit -m "Prepare for deployment"

# Push to Heroku
git push heroku main

# If you're on a different branch (e.g., master)
git push heroku master:main
```

### Step 5: Run Database Migrations

```bash
# Run migrations on Heroku
heroku run python manage.py migrate

# Collect static files (if not using AWS S3)
heroku run python manage.py collectstatic --noinput
```

### Step 6: Create Superuser

```bash
# Create admin user
heroku run python manage.py createsuperuser
```

### Step 7: Open Your Application

```bash
# Open the app in browser
heroku open

# Access admin panel
heroku open admin/
```

---

## ☁️ AWS S3 Configuration (Optional)

If you want to serve static and media files from AWS S3 instead of WhiteNoise:

### Step 1: Create AWS S3 Bucket

1. Go to AWS Console → S3
2. Click "Create bucket"
3. Choose a unique bucket name
4. Select your region
5. Uncheck "Block all public access"
6. Create bucket

### Step 2: Configure CORS Policy

Add this CORS configuration to your S3 bucket:

```json
[
    {
        "AllowedHeaders": ["*"],
        "AllowedMethods": ["GET", "HEAD", "PUT", "POST", "DELETE"],
        "AllowedOrigins": ["*"],
        "ExposeHeaders": []
    }
]
```

### Step 3: Create IAM User

1. Go to AWS Console → IAM
2. Create new user with programmatic access
3. Attach policy: `AmazonS3FullAccess`
4. Save Access Key ID and Secret Access Key

### Step 4: Update Environment Variables

```bash
heroku config:set USE_AWS=True
heroku config:set AWS_ACCESS_KEY_ID='your_access_key'
heroku config:set AWS_SECRET_ACCESS_KEY='your_secret_key'
heroku config:set AWS_STORAGE_BUCKET_NAME='your_bucket_name'
heroku config:set AWS_S3_REGION_NAME='your_region'
```

### Step 5: Redeploy and Collect Static Files

```bash
git push heroku main
heroku run python manage.py collectstatic --noinput
```

---

## 📝 Post-Deployment Tasks

### 1. Verify Deployment

```bash
# Check app logs
heroku logs --tail

# Run Django checks
heroku run python manage.py check --deploy
```

### 2. Test Core Functionality

- [ ] Homepage loads correctly
- [ ] User registration works
- [ ] User login/logout works
- [ ] Product browsing works
- [ ] Add to cart functionality
- [ ] Checkout process
- [ ] Payment processing (Stripe)
- [ ] Order confirmation emails
- [ ] Admin panel access

### 3. Set Up Monitoring (Recommended)

#### Error Tracking with Sentry

```bash
# Install Sentry
pip install sentry-sdk

# Add to requirements.txt
echo "sentry-sdk==2.14.0" >> requirements.txt

# Configure in settings.py
import sentry_sdk
sentry_sdk.init(
    dsn="your-sentry-dsn",
    environment="production",
)
```

#### Uptime Monitoring

- Set up uptime monitoring with services like:
  - UptimeRobot (free)
  - Pingdom
  - New Relic

### 4. Configure Custom Domain (Optional)

```bash
# Add custom domain
heroku domains:add www.your-domain.com

# Configure DNS records
# Add CNAME record: www -> your-app.herokuapp.com

# Update ALLOWED_HOSTS
heroku config:set ALLOWED_HOSTS='www.your-domain.com,your-domain.com,your-app.herokuapp.com'
```

### 5. Enable HTTPS/SSL

Heroku provides automatic SSL for `*.herokuapp.com` domains. For custom domains:

```bash
# Enable Automated Certificate Management (free)
heroku certs:auto:enable

# Or add your own SSL certificate
heroku certs:add server.crt server.key
```

### 6. Set Up Database Backups

```bash
# Schedule automatic backups
heroku pg:backups:schedule DATABASE_URL --at '02:00 America/Los_Angeles'

# Manual backup
heroku pg:backups:capture

# List backups
heroku pg:backups

# Download backup
heroku pg:backups:download
```

---

## 🔧 Troubleshooting

### Application Won't Start

```bash
# Check logs
heroku logs --tail

# Common issues:
# 1. Missing environment variables
heroku config

# 2. Database not configured
heroku addons

# 3. Static files not collected
heroku run python manage.py collectstatic --noinput
```

### Static Files Not Loading

**If using WhiteNoise:**
```bash
# Ensure WhiteNoise is in requirements.txt
grep whitenoise requirements.txt

# Collect static files
heroku run python manage.py collectstatic --noinput
```

**If using AWS S3:**
```bash
# Verify AWS credentials
heroku config:get AWS_ACCESS_KEY_ID
heroku config:get AWS_SECRET_ACCESS_KEY

# Check S3 bucket permissions and CORS
```

### Database Migration Issues

```bash
# Check migration status
heroku run python manage.py showmigrations

# Fake a migration (if needed)
heroku run python manage.py migrate --fake app_name migration_name

# Reset database (WARNING: deletes all data)
heroku pg:reset DATABASE_URL
heroku run python manage.py migrate
```

### Payment Processing Errors

```bash
# Verify Stripe keys
heroku config:get STRIPE_PUBLIC_KEY
heroku config:get STRIPE_SECRET_KEY

# Check Stripe dashboard for errors
# https://dashboard.stripe.com/logs

# Test with Stripe test cards
# https://stripe.com/docs/testing
```

### Email Not Sending

```bash
# Check email configuration
heroku config | grep EMAIL

# Test email sending
heroku run python manage.py shell
>>> from django.core.mail import send_mail
>>> send_mail('Test', 'Test message', 'from@example.com', ['to@example.com'])
```

### 500 Internal Server Error

```bash
# Enable DEBUG temporarily (ONLY for troubleshooting)
heroku config:set DEBUG=True

# Check logs for detailed error
heroku logs --tail

# IMPORTANT: Turn DEBUG off after fixing
heroku config:set DEBUG=False
```

---

## 📊 Performance Optimization

### 1. Enable Caching

Add to `requirements.txt`:
```
django-redis==5.4.0
```

Configure Redis caching (Heroku addon):
```bash
heroku addons:create heroku-redis:mini
```

### 2. Database Connection Pooling

Add to `requirements.txt`:
```
django-db-connection-pool==1.2.4
```

### 3. Compress Static Files

WhiteNoise already handles compression. For S3, enable gzip in settings.

### 4. CDN Configuration

Use CloudFront for AWS S3 or Cloudflare for better performance.

---

## 🔒 Security Checklist

- [ ] `DEBUG=False` in production
- [ ] Strong `SECRET_KEY` (50+ characters)
- [ ] `ALLOWED_HOSTS` properly configured
- [ ] HTTPS/SSL enabled
- [ ] Security headers configured (already in settings.py)
- [ ] CSRF protection enabled
- [ ] SQL injection protection (Django ORM)
- [ ] XSS protection enabled
- [ ] Secure password storage (Django default)
- [ ] Regular security updates

---

## 📚 Additional Resources

- [Django Deployment Checklist](https://docs.djangoproject.com/en/3.2/howto/deployment/checklist/)
- [Heroku Django Guide](https://devcenter.heroku.com/articles/django-app-configuration)
- [AWS S3 Django Guide](https://django-storages.readthedocs.io/en/latest/backends/amazon-S3.html)
- [Stripe Django Integration](https://stripe.com/docs/payments/accept-a-payment?platform=web&ui=elements)

---

## 🆘 Getting Help

If you encounter issues:

1. Check Heroku logs: `heroku logs --tail`
2. Review this troubleshooting guide
3. Check Django documentation
4. Search Heroku Dev Center
5. Contact support team

---

**Last Updated**: October 2025
**Django Version**: 3.2.25
**Python Version**: 3.12.7

