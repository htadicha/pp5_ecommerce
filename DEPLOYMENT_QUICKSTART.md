# ⚡ Quick Deployment Guide - Hawashmart

This is a condensed version of the full deployment guide for quick reference.

## 🚀 Deploy to Heroku in 5 Minutes

### 1. Generate Production SECRET_KEY
```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```
Copy the output - you'll need it in step 3.

### 2. Create Heroku App & Add Database
```bash
heroku create hawashmart-prod
heroku addons:create heroku-postgresql:essential-0
```

### 3. Set Environment Variables
```bash
# Replace 'YOUR_GENERATED_KEY' with the key from step 1
heroku config:set SECRET_KEY='YOUR_GENERATED_KEY'
heroku config:set DEBUG=False
heroku config:set ALLOWED_HOSTS='hawashmart-prod.herokuapp.com'

# Stripe keys - IMPORTANT: Use LIVE keys for production!
heroku config:set STRIPE_PUBLIC_KEY='pk_live_xxxxx'
heroku config:set STRIPE_SECRET_KEY='sk_live_xxxxx'
```

### 4. Deploy
```bash
git push heroku main
```

### 5. Run Migrations & Create Admin
```bash
heroku run python manage.py migrate
heroku run python manage.py createsuperuser
```

### 6. Open Your App
```bash
heroku open
```

---

## ✅ Pre-Deployment Checklist

Quick checklist before deploying:

```bash
# 1. Check for pending migrations
python manage.py makemigrations --check --dry-run

# 2. Run deployment checks
python manage.py check --deploy

# 3. Verify requirements.txt is up to date
pip freeze > requirements_check.txt
diff requirements.txt requirements_check.txt
rm requirements_check.txt

# 4. Test locally with DEBUG=False
# Update .env: DEBUG=False
python manage.py runserver
# Don't forget to set DEBUG=True again for development!

# 5. Ensure .env.example has no real secrets
cat .env.example
```

---

## 🔧 Common Heroku Commands

```bash
# View logs
heroku logs --tail

# Run Django shell
heroku run python manage.py shell

# Check config vars
heroku config

# Restart app
heroku restart

# Run migrations
heroku run python manage.py migrate

# Collect static files (if not using S3)
heroku run python manage.py collectstatic --noinput

# Access Django admin
heroku open admin/
```

---

## 🆘 Quick Fixes

### App Crashed
```bash
heroku logs --tail
heroku restart
```

### Database Issues
```bash
heroku run python manage.py migrate
heroku pg:info
```

### Static Files Not Loading
```bash
heroku run python manage.py collectstatic --noinput
# Or configure AWS S3 (see full deployment guide)
```

### Payment Not Working
- Check Stripe keys in `heroku config`
- Verify you're using LIVE keys (not test keys)
- Check Stripe dashboard for errors

---

## 📋 Environment Variables Quick Reference

| Variable | Required | Example |
|----------|----------|---------|
| SECRET_KEY | ✅ Yes | Auto-generated strong key |
| DEBUG | ✅ Yes | False |
| ALLOWED_HOSTS | ✅ Yes | your-app.herokuapp.com |
| DATABASE_URL | ✅ Yes | Auto-set by Heroku |
| STRIPE_PUBLIC_KEY | ✅ Yes | pk_live_xxxxx |
| STRIPE_SECRET_KEY | ✅ Yes | sk_live_xxxxx |
| USE_AWS | ❌ Optional | True/False |
| AWS_ACCESS_KEY_ID | ❌ Optional | If using S3 |
| AWS_SECRET_ACCESS_KEY | ❌ Optional | If using S3 |
| AWS_STORAGE_BUCKET_NAME | ❌ Optional | If using S3 |
| AWS_S3_REGION_NAME | ❌ Optional | If using S3 |
| EMAIL_BACKEND | ❌ Optional | For email sending |
| EMAIL_HOST | ❌ Optional | smtp.gmail.com |
| EMAIL_HOST_USER | ❌ Optional | your@email.com |
| EMAIL_HOST_PASSWORD | ❌ Optional | App password |

---

For complete deployment instructions, see [DEPLOYMENT.md](DEPLOYMENT.md)

