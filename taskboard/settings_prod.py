"""
Production settings for Railway deployment
"""
import os
import dj_database_url
from .settings import *

# Security settings
DEBUG = os.environ.get('DEBUG', 'False') == 'True'
SECRET_KEY = os.environ.get('SECRET_KEY', SECRET_KEY)

# Allowed hosts
ALLOWED_HOSTS = [
    '.railway.app',
    'taskboard-backend-production.up.railway.app',
    'localhost',
    '127.0.0.1',
]

# Add your Vercel frontend domain
FRONTEND_URL = os.environ.get('FRONTEND_URL', 'http://localhost:5173')

# CORS settings
CORS_ALLOWED_ORIGINS = [
    FRONTEND_URL,
    'http://localhost:5173',
    'http://localhost:3000',
]

CORS_ALLOW_CREDENTIALS = True

# Database - Railway provides DATABASE_URL
DATABASES = {
    'default': dj_database_url.config(
        default=f'sqlite:///{BASE_DIR / "db.sqlite3"}',
        conn_max_age=600
    )
}

# Static files (CSS, JavaScript, Images)
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

# WhiteNoise configuration for serving static files
MIDDLEWARE.insert(1, 'whitenoise.middleware.WhiteNoiseMiddleware')
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# Security settings for production
if not DEBUG:
    SECURE_SSL_REDIRECT = True
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    SECURE_BROWSER_XSS_FILTER = True
    SECURE_CONTENT_TYPE_NOSNIFF = True
