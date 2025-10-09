from pathlib import Path
import os
import dj_database_url

# -------------------------------
# PATHS
# -------------------------------
BASE_DIR = Path(__file__).resolve().parent.parent

# -------------------------------
# SECURITY SETTINGS
# -------------------------------
SECRET_KEY = os.environ.get(
    'DJANGO_SECRET_KEY',
    'django-insecure-nh5fofm#p5i8#e+zf&-au1x&=kqcjgw)kx4cgo#)f@4_5dw)ww'
)

# Default DEBUG to False in production
DEBUG = os.environ.get('DEBUG', 'False') == 'True'

# Hosts allowed to access the app
ALLOWED_HOSTS = [
    'project3rb-d3edfb5c8d9d.herokuapp.com',
    'localhost',
    '127.0.0.1',
]

# ✅ TEMPORARY: Allow iframe embedding for Am I Responsive screenshot
X_FRAME_OPTIONS = 'ALLOWALL'

# -------------------------------
# INSTALLED APPS
# -------------------------------
INSTALLED_APPS = [
    # Django default apps
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Third-party apps
    'rest_framework',
    'widget_tweaks',

    # Local apps
    'homepageapp',
]

# -------------------------------
# MIDDLEWARE
# -------------------------------
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',  # Handles static files in production
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# -------------------------------
# URL CONFIGURATION
# -------------------------------
ROOT_URLCONF = 'project3rb.urls'

# -------------------------------
# TEMPLATES
# -------------------------------
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],  # optional templates folder
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

# -------------------------------
# WSGI
# -------------------------------
WSGI_APPLICATION = 'project3rb.wsgi.application'

# -------------------------------
# DATABASES
# -------------------------------
# Use Heroku Postgres in production, fallback to local PostgreSQL
if os.environ.get('DATABASE_URL'):
    DATABASES = {
        'default': dj_database_url.config(
            default=os.environ['DATABASE_URL'],
            conn_max_age=600,
            ssl_require=True
        )
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': 'project3rb',
            'USER': 'JermaineMckenna',
            'PASSWORD': 'Morgan7890',
            'HOST': 'localhost',
            'PORT': '5432',
        }
    }

# -------------------------------
# PASSWORD VALIDATION
# -------------------------------
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# -------------------------------
# INTERNATIONALIZATION
# -------------------------------
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'Europe/London'  # ✅ Matches your restaurant timezone
USE_I18N = True
USE_TZ = True

# -------------------------------
# STATIC FILES
# -------------------------------
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# -------------------------------
# MEDIA FILES (if used later)
# -------------------------------
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# -------------------------------
# DEFAULT PRIMARY KEY FIELD
# -------------------------------
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# -------------------------------
# GOOGLE CALENDAR / API CONFIG
# -------------------------------
# These credentials are stored securely in Heroku config vars
GOOGLE_CALENDAR_ID = 'restaurantbookingproject@restaurant-booking-calendar.iam.gserviceaccount.com'
GOOGLE_TIMEZONE = 'Europe/London'
GOOGLE_CREDS = os.environ.get("GOOGLE_CREDS")
