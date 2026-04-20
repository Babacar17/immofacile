"""
Paramètres de PRODUCTION pour Render.com
"""
from .settings import *
from decouple import config

# ── Sécurité ──────────────────────────────────────────────────────────────────
DEBUG      = False
SECRET_KEY = config('SECRET_KEY')

# Render génère un sous-domaine *.onrender.com + votre domaine custom éventuel
ALLOWED_HOSTS = config('ALLOWED_HOSTS', default='').split(',')

# Render gère déjà le HTTPS via proxy — pas besoin de redirection Django
SECURE_SSL_REDIRECT            = False   # Render s'en occupe
SECURE_PROXY_SSL_HEADER        = ('HTTP_X_FORWARDED_PROTO', 'https')
SECURE_BROWSER_XSS_FILTER      = True
SECURE_CONTENT_TYPE_NOSNIFF    = True
SESSION_COOKIE_SECURE          = True
CSRF_COOKIE_SECURE             = True
X_FRAME_OPTIONS                = 'DENY'
SECURE_HSTS_SECONDS            = 31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS = True

# ── Base de données PostgreSQL ────────────────────────────────────────────────
DATABASES = {
    'default': {
        'ENGINE':   'django.db.backends.postgresql',
        'NAME':     config('DB_NAME'),
        'USER':     config('DB_USER'),
        'PASSWORD': config('DB_PASSWORD'),
        'HOST':     config('DB_HOST'),
        'PORT':     config('DB_PORT', default='5432'),
        'CONN_MAX_AGE': 60,
        'OPTIONS':  {'sslmode': 'require'},
    }
}

# ── Fichiers statiques — WhiteNoise ───────────────────────────────────────────
MIDDLEWARE.insert(1, 'whitenoise.middleware.WhiteNoiseMiddleware')
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
STATIC_ROOT = BASE_DIR / 'staticfiles'

# ── Email (optionnel — console si non configuré) ─────────────────────────────
_email_user = config('EMAIL_HOST_USER', default='')
if _email_user:
    EMAIL_BACKEND       = 'django.core.mail.backends.smtp.EmailBackend'
    EMAIL_HOST          = config('EMAIL_HOST', default='smtp.gmail.com')
    EMAIL_PORT          = config('EMAIL_PORT', default=587, cast=int)
    EMAIL_USE_TLS       = True
    EMAIL_HOST_USER     = _email_user
    EMAIL_HOST_PASSWORD = config('EMAIL_HOST_PASSWORD', default='')
    DEFAULT_FROM_EMAIL  = config('DEFAULT_FROM_EMAIL', default='ImmoFacile <noreply@immofacile.sn>')
else:
    EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# ── Logging allégé en production ──────────────────────────────────────────────
LOGGING['handlers']['console']['level'] = 'WARNING'
