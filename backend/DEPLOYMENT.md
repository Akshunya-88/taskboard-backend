# TaskBoard Backend - Deployment Guide

## Railway Deployment Instructions

### 1. Prepare Your Repository
```bash
cd /Users/akshunya/Desktop/Task-Manager/taskboard-backend
git init
git add .
git commit -m "Initial commit for Railway deployment"
```

### 2. Create a Railway Account
1. Go to [railway.app](https://railway.app)
2. Sign up with GitHub

### 3. Deploy to Railway
1. Click "New Project"
2. Select "Deploy from GitHub repo"
3. Connect your GitHub account and select the backend repository
4. Railway will auto-detect Django and deploy

### 4. Add PostgreSQL Database
1. In your Railway project, click "New"
2. Select "Database" → "Add PostgreSQL"
3. Railway will automatically set the `DATABASE_URL` environment variable

### 5. Configure Environment Variables
In Railway project settings, add these variables:
- `DJANGO_SETTINGS_MODULE` = `taskboard.settings_prod`
- `SECRET_KEY` = (generate a secure key: `python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"`)
- `DEBUG` = `False`
- `FRONTEND_URL` = (your Vercel URL, e.g., `https://your-app.vercel.app`)

### 6. Run Migrations
In Railway's project terminal, run:
```bash
python manage.py migrate
python manage.py createsuperuser
```

### 7. Collect Static Files
```bash
python manage.py collectstatic --noinput
```

### 8. Get Your Backend URL
Railway will provide a URL like: `https://your-app.railway.app`

---

## Frontend Configuration
After deployment, update your frontend `.env` with:
```
VITE_API_BASE_URL=https://your-backend.railway.app/api
```
