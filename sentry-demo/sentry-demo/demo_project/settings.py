"""
Django settings for Sentry demo project.

🔑 SENTRY ENTEGRASYONU AŞAĞIDA — sunumda bu bölümü göster!
"""

import os
from pathlib import Path

# ============================================================
# SENTRY ENTEGRASYONU (⭐ Sunumda göstereceğin kritik kod)
# ============================================================
import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration

SENTRY_DSN = os.environ.get("SENTRY_DSN", "")

if SENTRY_DSN:
    sentry_sdk.init(
        dsn=SENTRY_DSN,

        # Django ile otomatik entegrasyon:
        # - Tüm unhandled exception'ları yakalar
        # - Request/response bilgisini ekler
        # - Database query'lerini tracing'e ekler
        integrations=[DjangoIntegration()],

        # Performance monitoring:
        # 1.0 = tüm transaction'ları kaydet (demo için ideal)
        # Production'da 0.1-0.2 önerilir (maliyet kontrolü)
        traces_sample_rate=1.0,

        # Kullanıcı IP, cookie vb. bilgileri gönder
        # Production'da KVKK/GDPR için dikkatli kullan!
        send_default_pii=True,

        # Release takibi (hangi sürümde hata oldu?)
        release=os.environ.get("SENTRY_RELEASE", "demo@1.0.0"),

        # Ortam ayrımı (dev/staging/prod)
        environment=os.environ.get("SENTRY_ENVIRONMENT", "development"),
    )
    print(f"✅ Sentry aktif: {SENTRY_DSN[:40]}...")
else:
    print("⚠️  SENTRY_DSN ayarlı değil — Sentry devre dışı!")

# ============================================================
# Standart Django ayarları
# ============================================================

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = "django-insecure-demo-key-DO-NOT-USE-IN-PRODUCTION"
DEBUG = True
ALLOWED_HOSTS = ["*"]

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "demo_app",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "demo_project.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
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

WSGI_APPLICATION = "demo_project.wsgi.application"

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}

LANGUAGE_CODE = "tr"
TIME_ZONE = "Europe/Istanbul"
USE_I18N = True
USE_TZ = True

STATIC_URL = "static/"
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
