# Render Deployment Guide for Swiggy Clone

## ✅ Completed Configuration Steps

### 1. **Django Settings Updated** ✓
- Environment variable support added
- Production security settings configured
- Database configuration updated for PostgreSQL
- Static files configuration optimized
- WhiteNoise middleware added

### 2. **Deployment Files Created** ✓
- **Procfile**: Defines how Render runs your app
- **runtime.txt**: Specifies Python 3.11.8
- **build.sh**: Runs migrations and collects static files
- **.env.example**: Template for environment variables
- **requirements_prod.txt**: Production dependencies

---

## 📋 Step-by-Step Deployment Instructions

### Step 1: Prepare Your Git Repository
```bash
# Initialize git if not already done
git init

# Add all files
git add .

# Commit
git commit -m "Initial deployment setup"

# Add remote (replace with your GitHub URL)
git remote add origin https://github.com/YOUR_USERNAME/swiggy-clone.git

# Push to GitHub
git branch -M main
git push -u origin main
```

### Step 2: Create Environment Variables
On Render dashboard, set these in the Environment tab:

```
SECRET_KEY=<generate a new secret key>
DEBUG=False
ALLOWED_HOSTS=your-app-name.onrender.com,www.your-app-name.onrender.com
USE_POSTGRESQL=True
DATABASE_URL=<Render will auto-fill this>
```

**To generate a new SECRET_KEY:**
```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

### Step 3: Create PostgreSQL Database (Optional but Recommended)
1. In Render dashboard, create a new PostgreSQL database
2. Render will provide DATABASE_URL automatically
3. Add to environment variables

### Step 4: Deploy to Render

#### Option A: Direct Connection (Easiest)
1. Go to [Render.com](https://render.com)
2. Click "New +" → "Web Service"
3. Select "Deploy an existing repository"
4. Connect your GitHub account and select your repo
5. Fill in details:
   - **Name**: swiggy-clone (or your preference)
   - **Environment**: Python 3
   - **Build Command**: `pip install -r requirements_prod.txt && python manage.py collectstatic --noinput`
   - **Start Command**: `gunicorn swiggy_clone.wsgi:application`
   - **Instance Type**: Free tier (for testing)
6. Add environment variables
7. Click "Create Web Service"

#### Option B: Using Render Native Postgres
1. In same dashboard, create a PostgreSQL instance
2. Link it to your web service
3. Render auto-adds DATABASE_URL

### Step 5: Monitor Deployment
```bash
# View logs in Render dashboard or use:
render logs <service-id>
```

### Step 6: Run Migrations (First Time Only)
```bash
# Via Render Shell:
python manage.py migrate

# Or via one-time command in Render dashboard
```

---

## 🔧 Important Configuration Notes

### Static Files
- WhiteNoise will serve static files automatically
- Run `python manage.py collectstatic` before deployment
- CSS/JS/images go in the `static/` folder

### Media Files
- Render filesystem is ephemeral (resets on redeploy)
- **For production**: Use AWS S3 or Render Disk
- Install: `pip install django-storages boto3`

### Database
- SQLite won't work on Render (ephemeral)
- Use PostgreSQL for persistence
- Migrations run automatically via Procfile

---

## 🐛 Troubleshooting

### Error: "ModuleNotFoundError: No module named 'gunicorn'"
**Solution**: Check requirements_prod.txt includes all packages

### Error: "ALLOWED_HOSTS Error"
**Solution**: Update ALLOWED_HOSTS in environment variables

### Error: "Static files not loading"
**Solution**: Run `python manage.py collectstatic --noinput`

### Error: "Database connection error"
**Solution**: Verify DATABASE_URL in environment variables

---

## 📊 Pre-Deployment Checklist

- [ ] All code committed to GitHub
- [ ] requirements_prod.txt updated
- [ ] SECRET_KEY changed (never use insecure one)
- [ ] DEBUG = False in environment
- [ ] ALLOWED_HOSTS set correctly
- [ ] Procfile exists
- [ ] runtime.txt exists
- [ ] Database selected (PostgreSQL recommended)
- [ ] Static files configuration verified
- [ ] Media files plan decided

---

## 🚀 After Deployment

1. Test your application URL
2. Check admin panel: `your-url/admin`
3. Monitor logs for errors
4. Set up monitoring/alerts on Render

---

## 📞 Helpful Links
- [Render Docs](https://render.com/docs)
- [Django Deployment Checklist](https://docs.djangoproject.com/en/6.0/howto/deployment/checklist/)
- [Gunicorn Docs](https://gunicorn.org/)

