from pathlib import Path

import environ

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Initialize django-environ
env = environ.Env(
    DEBUG=(bool, False),
    ALLOWED_HOSTS=(list, []),
    DATABASE_URL=(str, ""),
)

# Read .env file (12-factor compliance)
environ.Env.read_env(BASE_DIR / ".env")

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env("SECRET_KEY")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = env("DEBUG")

ALLOWED_HOSTS = env("ALLOWED_HOSTS")

# Application definition
DJANGO_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
]

THIRD_PARTY_APPS = [
    "django_extensions",
]

LOCAL_APPS = [
    "apps.accounts",
    "patient",
    "patient_risk",
]

INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + LOCAL_APPS

# Add debug toolbar in development if available
if DEBUG:
    try:
        import debug_toolbar

        INSTALLED_APPS += ["debug_toolbar"]
    except ImportError:
        pass

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

# Add debug toolbar middleware in development if available
if DEBUG:
    try:
        import debug_toolbar

        MIDDLEWARE += ["debug_toolbar.middleware.DebugToolbarMiddleware"]
    except ImportError:
        pass

ROOT_URLCONF = "core.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "core.wsgi.application"
ASGI_APPLICATION = "core.asgi.application"

# Database (12-factor compliant)
# https://docs.djangoproject.com/en/5.2/ref/settings/#databases
DATABASES = {"default": env.db()}

# Default primary key field type
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]

# Internationalization
LANGUAGE_CODE = env("LANGUAGE_CODE", default="en-us")
TIME_ZONE = env("TIME_ZONE", default="UTC")
USE_I18N = True
USE_TZ = True

# Static files (CSS, JavaScript, Images)
STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "staticfiles"
STATICFILES_DIRS = [BASE_DIR / "static"]

# Media files
MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"

# Security settings (12-factor compliant)
SECURE_BROWSER_XSS_FILTER = env("SECURE_BROWSER_XSS_FILTER", default=True)
SECURE_CONTENT_TYPE_NOSNIFF = env("SECURE_CONTENT_TYPE_NOSNIFF", default=True)
X_FRAME_OPTIONS = env("X_FRAME_OPTIONS", default="DENY")
SECURE_HSTS_SECONDS = env("SECURE_HSTS_SECONDS", default=31536000, cast=int)
SECURE_HSTS_INCLUDE_SUBDOMAINS = env("SECURE_HSTS_INCLUDE_SUBDOMAINS", default=True)
SECURE_HSTS_PRELOAD = env("SECURE_HSTS_PRELOAD", default=True)

# Session configuration
SESSION_COOKIE_SECURE = env("SESSION_COOKIE_SECURE", default=not DEBUG)
SESSION_COOKIE_HTTPONLY = env("SESSION_COOKIE_HTTPONLY", default=True)
SESSION_COOKIE_AGE = env("SESSION_COOKIE_AGE", default=3600, cast=int)

# CSRF configuration
CSRF_COOKIE_SECURE = env("CSRF_COOKIE_SECURE", default=not DEBUG)
CSRF_COOKIE_HTTPONLY = env("CSRF_COOKIE_HTTPONLY", default=True)

# Authentication URLs
LOGIN_URL = "/"
LOGIN_REDIRECT_URL = "/patient/"

# Debug toolbar configuration (development only)
if DEBUG:
    INTERNAL_IPS = [
        "127.0.0.1",
        "0.0.0.0",
    ]

# Logging Configuration (12-Factor Compliant)
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "verbose": {
            "format": "{levelname} {asctime} {module} {process:d} {thread:d} {message}",
            "style": "{",
        },
        "simple": {
            "format": "{levelname} {message}",
            "style": "{",
        },
        "json": {
            "format": "{levelname} {asctime} {module} {message}",
            "style": "{",
        },
    },
    "handlers": {
        "console": {
            "level": env("LOG_LEVEL", default="INFO"),
            "class": "logging.StreamHandler",
            "formatter": "verbose" if DEBUG else "json",
        },
        "file": {
            "level": "INFO",
            "class": "logging.handlers.RotatingFileHandler",
            "filename": BASE_DIR / "logs" / "django.log",
            "maxBytes": 1024 * 1024 * 15,  # 15MB
            "backupCount": 10,
            "formatter": "json",
        },
    },
    "root": {
        "handlers": ["console"],
        "level": env("LOG_LEVEL", default="INFO"),
    },
    "loggers": {
        "django": {
            "handlers": ["console", "file"] if not DEBUG else ["console"],
            "level": env("LOG_LEVEL", default="INFO"),
            "propagate": False,
        },
        "core": {
            "handlers": ["console", "file"] if not DEBUG else ["console"],
            "level": env("LOG_LEVEL", default="INFO"),
            "propagate": False,
        },
    },
}

# Email configuration (12-factor compliant)
EMAIL_BACKEND = env(
    "EMAIL_BACKEND", default="django.core.mail.backends.console.EmailBackend"
)
if not DEBUG:
    EMAIL_HOST = env("EMAIL_HOST", default="")
    EMAIL_PORT = env("EMAIL_PORT", default=587, cast=int)
    EMAIL_USE_TLS = env("EMAIL_USE_TLS", default=True, cast=bool)
    EMAIL_HOST_USER = env("EMAIL_HOST_USER", default="")
    EMAIL_HOST_PASSWORD = env("EMAIL_HOST_PASSWORD", default="")

# Cache configuration (12-factor compliant)
CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.locmem.LocMemCache",
    }
}

# Production-specific settings
if not DEBUG:
    # Force HTTPS
    SECURE_SSL_REDIRECT = env("SECURE_SSL_REDIRECT", default=True, cast=bool)
    SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")

    # Additional security headers
    SECURE_REFERRER_POLICY = "strict-origin-when-cross-origin"

    # Static files optimization
    STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"
