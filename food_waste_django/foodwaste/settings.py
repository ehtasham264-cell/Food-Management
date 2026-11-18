import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = os.environ.get("DJANGO_SECRET_KEY", "django-insecure-local-development-only-key")
DEBUG = os.environ.get("DJANGO_DEBUG", "False").lower() == "true"

# Set VERCEL=1 automatically in the Vercel project environment.
ON_VERCEL = os.environ.get("VERCEL", "").lower() == "1"

ALLOWED_HOSTS = [host.strip() for host in os.environ.get("DJANGO_ALLOWED_HOSTS", "localhost,127.0.0.1").split(",") if host.strip()]
if ON_VERCEL:
    ALLOWED_HOSTS += [".vercel.app"]

CSRF_TRUSTED_ORIGINS = [origin.strip() for origin in os.environ.get("CSRF_TRUSTED_ORIGINS", "").split(",") if origin.strip()]
if ON_VERCEL:
    CSRF_TRUSTED_ORIGINS += ["https://*.vercel.app"]

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "tracker",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
]

ROOT_URLCONF = "foodwaste.urls"

TEMPLATES = [{
    "BACKEND": "django.template.backends.django.DjangoTemplates",
    "DIRS": [],
    "APP_DIRS": True,
    "OPTIONS": {"context_processors": [
        "django.template.context_processors.request",
        "django.contrib.auth.context_processors.auth",
        "django.contrib.messages.context_processors.messages",
    ]},
}]

WSGI_APPLICATION = "foodwaste.wsgi.application"

# SQLite is suitable for local development only. On Vercel, configure DATABASE_URL
# with a managed PostgreSQL database (for example Neon) because serverless filesystems
# are ephemeral and cannot safely hold your production database.
DATABASE_URL = os.environ.get("DATABASE_URL")
if DATABASE_URL:
    try:
        import dj_database_url
    except ImportError as exc:
        raise RuntimeError("Install dj-database-url to use DATABASE_URL") from exc
    DATABASES = {"default": dj_database_url.parse(DATABASE_URL, conn_max_age=0, ssl_require=True)}
else:
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": BASE_DIR / "db.sqlite3",
        }
    }

LANGUAGE_CODE = "en-us"
TIME_ZONE = "Asia/Kolkata"
USE_I18N = True
USE_TZ = True

STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "staticfiles"

# Vercel runs collectstatic at build time and serves these files via its CDN.
# WhiteNoise is used for local production-like runs and as a fallback.
if not ON_VERCEL:
    try:
        import whitenoise  # noqa: F401
        MIDDLEWARE.insert(1, "whitenoise.middleware.WhiteNoiseMiddleware")
        STORAGES = {
            "default": {"BACKEND": "django.core.files.storage.FileSystemStorage"},
            "staticfiles": {"BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage"},
        }
    except ImportError:
        pass

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# Basic production security settings.
if not DEBUG:
    SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
    SESSION_COOKIE_SECURE = ON_VERCEL
    CSRF_COOKIE_SECURE = ON_VERCEL
