from pathlib import Path
from decouple import config

BASE_DIR = Path(__file__).resolve().parent.parent
LOGS_DIR = BASE_DIR / 'logs'
LOGS_DIR.mkdir(exist_ok=True)

SECRET_KEY    = config('SECRET_KEY', default='django-insecure-immofacile-dev-key-changez-en-prod')
DEBUG         = config('DEBUG', default=True, cast=bool)
ALLOWED_HOSTS = config('ALLOWED_HOSTS', default='*').split(',')

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.humanize',
    'django_filters',
    'core',
    'accounts',
    'listings',
    'agencies',
    'messaging',
    'dashboard',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'core.middleware.RequestLoggingMiddleware',
]

ROOT_URLCONF = 'immofacile.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'core.context_processors.site_settings',
            ],
        },
    },
]

WSGI_APPLICATION = 'immofacile.wsgi.application'

# ── Base de données ───────────────────────────────────────────────────────────
# SQLite par défaut (dev). Pour PostgreSQL, définir les variables d'env.
DATABASES = {
    'default': {
        'ENGINE':  config('DB_ENGINE',   default='django.db.backends.sqlite3'),
        'NAME':    config('DB_NAME',     default=str(BASE_DIR / 'db.sqlite3')),
        'USER':    config('DB_USER',     default=''),
        'PASSWORD':config('DB_PASSWORD', default=''),
        'HOST':    config('DB_HOST',     default=''),
        'PORT':    config('DB_PORT',     default=''),
        'CONN_MAX_AGE': 60,
    }
}

# ── Auth ──────────────────────────────────────────────────────────────────────
AUTH_USER_MODEL     = 'accounts.User'
LOGIN_URL           = '/accounts/connexion/'
LOGIN_REDIRECT_URL  = '/'
LOGOUT_REDIRECT_URL = '/'

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator', 'OPTIONS': {'min_length': 8}},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

SESSION_COOKIE_AGE = 60 * 60 * 24 * 30  # 30 jours

# ── Localisation ──────────────────────────────────────────────────────────────
LANGUAGE_CODE = 'fr-fr'
TIME_ZONE     = 'Africa/Dakar'
USE_I18N      = True
USE_TZ        = True

# ── Fichiers ──────────────────────────────────────────────────────────────────
STATIC_URL       = '/static/'
STATICFILES_DIRS = [BASE_DIR / 'static']
STATIC_ROOT      = BASE_DIR / 'staticfiles'
MEDIA_URL        = '/media/'
MEDIA_ROOT       = BASE_DIR / 'media'

DATA_UPLOAD_MAX_MEMORY_SIZE = 10 * 1024 * 1024   # 10 Mo
FILE_UPLOAD_MAX_MEMORY_SIZE = 10 * 1024 * 1024

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# ── Email ─────────────────────────────────────────────────────────────────────
EMAIL_BACKEND      = config('EMAIL_BACKEND', default='django.core.mail.backends.console.EmailBackend')
EMAIL_HOST         = config('EMAIL_HOST',    default='smtp.gmail.com')
EMAIL_PORT         = config('EMAIL_PORT',    default=587, cast=int)
EMAIL_USE_TLS      = True
EMAIL_HOST_USER    = config('EMAIL_HOST_USER',    default='')
EMAIL_HOST_PASSWORD= config('EMAIL_HOST_PASSWORD',default='')
DEFAULT_FROM_EMAIL = 'ImmoFacile <noreply@immofacile.sn>'

# ── Logging ───────────────────────────────────────────────────────────────────
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{asctime} [{levelname}] {name} — {message}',
            'style': '{', 'datefmt': '%Y-%m-%d %H:%M:%S',
        },
        'simple': {
            'format': '{asctime} [{levelname}] {message}',
            'style': '{', 'datefmt': '%H:%M:%S',
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'simple',
            'level': 'DEBUG',
        },
        'file_app': {
            'class': 'logging.handlers.TimedRotatingFileHandler',
            'filename': str(LOGS_DIR / 'app.log'),
            'when': 'midnight', 'backupCount': 30,
            'encoding': 'utf-8', 'formatter': 'verbose', 'level': 'INFO',
        },
        'file_errors': {
            'class': 'logging.handlers.TimedRotatingFileHandler',
            'filename': str(LOGS_DIR / 'errors.log'),
            'when': 'midnight', 'backupCount': 60,
            'encoding': 'utf-8', 'formatter': 'verbose', 'level': 'ERROR',
        },
        'file_requests': {
            'class': 'logging.handlers.TimedRotatingFileHandler',
            'filename': str(LOGS_DIR / 'requests.log'),
            'when': 'midnight', 'backupCount': 14,
            'encoding': 'utf-8', 'formatter': 'verbose', 'level': 'INFO',
        },
        'file_security': {
            'class': 'logging.handlers.TimedRotatingFileHandler',
            'filename': str(LOGS_DIR / 'security.log'),
            'when': 'midnight', 'backupCount': 90,
            'encoding': 'utf-8', 'formatter': 'verbose', 'level': 'WARNING',
        },
    },
    'loggers': {
        'immofacile': {
            'handlers': ['console', 'file_app', 'file_errors'],
            'level': 'DEBUG', 'propagate': False,
        },
        'immofacile.requests': {
            'handlers': ['file_requests'],
            'level': 'INFO', 'propagate': False,
        },
        'immofacile.security': {
            'handlers': ['console', 'file_security'],
            'level': 'WARNING', 'propagate': False,
        },
        'django': {
            'handlers': ['console', 'file_errors'],
            'level': 'WARNING', 'propagate': False,
        },
    },
}
