"""
Django settings for Hawashmart project.
"""

from pathlib import Path
import os
from decouple import config
import dj_database_url
from django.core.exceptions import ImproperlyConfigured

BASE_DIR = Path(__file__).resolve().parent.parent

# The SECRET_KEY is now read from your .env file or Heroku Config Vars
SECRET_KEY = config("SECRET_KEY")

# DEBUG is False in production for security. It will be True locally if set in .env
DEBUG = config("DEBUG", default=False, cast=bool)

# ALLOWED_HOSTS is read from environment variables.
ALLOWED_HOSTS = config(
    "ALLOWED_HOSTS", cast=lambda v: [s.strip() for s in v.split(",")]
)


# Application definition
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "accounts",
    "category",
    "store",
    "carts",
    "orders",
    "storages",  # For AWS S3
    "admin_thumbnails",
    "django_ckeditor_5",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    # Add WhiteNoise middleware here, right after the security middleware
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "Hawashmart.urls"

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
                "category.context_processors.menu_links",
                "carts.context_processors.counter",
            ],
        },
    },
]

WSGI_APPLICATION = "Hawashmart.wsgi.application"
AUTH_USER_MODEL = "accounts.Account"


# Database Configuration
# Uses dj_database_url to parse DATABASE_URL with a safe SQLite fallback
DATABASE_URL = config("DATABASE_URL", default=f"sqlite:///{BASE_DIR / 'db.sqlite3'}")
DATABASES = {
    "default": dj_database_url.config(
        default=DATABASE_URL,
        conn_max_age=600,
        ssl_require=not DEBUG,
    )
}


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
LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_L10N = True
USE_TZ = True


# Static and Media files configuration
USE_AWS = config("USE_AWS", default=False, cast=bool)

if USE_AWS:
    # AWS S3 Configuration for Production - Media files only
    AWS_ACCESS_KEY_ID = config("AWS_ACCESS_KEY_ID")
    AWS_SECRET_ACCESS_KEY = config("AWS_SECRET_ACCESS_KEY")
    AWS_STORAGE_BUCKET_NAME = config("AWS_STORAGE_BUCKET_NAME")
    # Extract region code (e.g., 'eu-west-1' from 'Europe (Ireland) eu-west-1')
    region_config = config("AWS_S3_REGION_NAME")
    AWS_S3_REGION_NAME = region_config.split()[-1] if region_config else "eu-west-1"
    AWS_S3_CUSTOM_DOMAIN = f"{AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com"
    AWS_S3_FILE_OVERWRITE = False
    # AWS_DEFAULT_ACL is set by MediaStorage class, don't override here
    AWS_QUERYSTRING_AUTH = (
        False  # Don't use query string authentication for public files
    )
    AWS_S3_OBJECT_PARAMETERS = {
        "CacheControl": "max-age=86400",
    }

    # Media files go to S3 with public-read access
    # Note: Must use 'Hawashmart' (capital H) to match the directory name
    DEFAULT_FILE_STORAGE = "Hawashmart.custom_storages.MediaStorage"
    MEDIA_URL = f"https://{AWS_S3_CUSTOM_DOMAIN}/media/"
    MEDIA_ROOT = BASE_DIR / "media"

    # Static files use WhiteNoise (works better on Heroku)
    STATIC_URL = "/static/"
    STATIC_ROOT = BASE_DIR / "staticfiles"
    STATICFILES_DIRS = [
        BASE_DIR / "static",
    ]
    # Use Django's default storage - WhiteNoise middleware handles compression
    STATICFILES_STORAGE = "django.contrib.staticfiles.storage.StaticFilesStorage"

    # WhiteNoise configuration for better static file serving
    WHITENOISE_USE_FINDERS = True  # Allow WhiteNoise to find files in STATICFILES_DIRS
    WHITENOISE_AUTOREFRESH = True  # Auto-refresh in development
else:
    # Local Static and Media files configuration
    STATIC_URL = "/static/"
    STATIC_ROOT = BASE_DIR / "staticfiles"
    STATICFILES_DIRS = [
        BASE_DIR / "static",
    ]
    MEDIA_URL = "/media/"
    MEDIA_ROOT = BASE_DIR / "media"
    # Use Django's default storage - WhiteNoise middleware handles compression
    STATICFILES_STORAGE = "django.contrib.staticfiles.storage.StaticFilesStorage"

    # WhiteNoise configuration for better static file serving
    WHITENOISE_USE_FINDERS = True  # Allow WhiteNoise to find files in STATICFILES_DIRS
    WHITENOISE_AUTOREFRESH = True  # Auto-refresh in development


# Default primary key field type
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# Stripe Keys from environment variables
STRIPE_PUBLIC_KEY = config("STRIPE_PUBLIC_KEY")
STRIPE_SECRET_KEY = config("STRIPE_SECRET_KEY")


# CKEditor 5 Configuration
CKEDITOR_5_CONFIGS = {
    "default": {
        "toolbar": [
            "heading",
            "|",
            "bold",
            "italic",
            "link",
            "bulletedList",
            "numberedList",
            "blockQuote",
            "imageUpload",
        ],
    },
    "extends": {
        "blockToolbar": [
            "paragraph",
            "heading1",
            "heading2",
            "heading3",
            "|",
            "bulletedList",
            "numberedList",
            "|",
            "blockQuote",
        ],
        "toolbar": [
            "heading",
            "|",
            "outdent",
            "indent",
            "|",
            "bold",
            "italic",
            "link",
            "underline",
            "strikethrough",
            "code",
            "subscript",
            "superscript",
            "highlight",
            "|",
            "codeBlock",
            "sourceEditing",
            "insertImage",
            "bulletedList",
            "numberedList",
            "todoList",
            "|",
            "blockQuote",
            "imageUpload",
            "|",
            "fontSize",
            "fontFamily",
            "fontColor",
            "fontBackgroundColor",
            "mediaEmbed",
            "removeFormat",
            "insertTable",
        ],
        "image": {
            "toolbar": [
                "imageTextAlternative",
                "|",
                "imageStyle:alignLeft",
                "imageStyle:alignRight",
                "imageStyle:alignCenter",
                "imageStyle:side",
                "|",
            ],
            "styles": [
                "full",
                "side",
                "alignLeft",
                "alignRight",
                "alignCenter",
            ],
        },
        "table": {
            "contentToolbar": [
                "tableColumn",
                "tableRow",
                "mergeTableCells",
                "tableProperties",
                "tableCellProperties",
            ],
        },
        "heading": {
            "options": [
                {
                    "model": "paragraph",
                    "title": "Paragraph",
                    "class": "ck-heading_paragraph",
                },
                {
                    "model": "heading1",
                    "view": "h1",
                    "title": "Heading 1",
                    "class": "ck-heading_heading1",
                },
                {
                    "model": "heading2",
                    "view": "h2",
                    "title": "Heading 2",
                    "class": "ck-heading_heading2",
                },
                {
                    "model": "heading3",
                    "view": "h3",
                    "title": "Heading 3",
                    "class": "ck-heading_heading3",
                },
            ]
        },
    },
}

# Email configuration
DEFAULT_EMAIL_BACKEND = (
    "django.core.mail.backends.console.EmailBackend"
    if DEBUG
    else "django.core.mail.backends.smtp.EmailBackend"
)
EMAIL_BACKEND = config("EMAIL_BACKEND", default=DEFAULT_EMAIL_BACKEND)
EMAIL_HOST = config("EMAIL_HOST", default=None)
EMAIL_PORT = config("EMAIL_PORT", default=587, cast=int)
EMAIL_USE_TLS = config("EMAIL_USE_TLS", default=True, cast=bool)
EMAIL_HOST_USER = config("EMAIL_HOST_USER", default=None)
EMAIL_HOST_PASSWORD = config("EMAIL_HOST_PASSWORD", default=None)
DEFAULT_FROM_EMAIL = config(
    "DEFAULT_FROM_EMAIL", default=EMAIL_HOST_USER or "noreply@hawashmart.com"
)

if not DEBUG and EMAIL_BACKEND.endswith("smtp.EmailBackend"):
    missing_settings = [
        name
        for name, value in {
            "EMAIL_HOST": EMAIL_HOST,
            "EMAIL_HOST_USER": EMAIL_HOST_USER,
            "EMAIL_HOST_PASSWORD": EMAIL_HOST_PASSWORD,
        }.items()
        if not value
    ]
    if missing_settings:
        missing = ", ".join(missing_settings)
        raise ImproperlyConfigured(
            f"SMTP email backend is configured but missing required settings: {missing}"
        )

# Production Security Settings
if not DEBUG:
    # Security settings for production
    SECURE_BROWSER_XSS_FILTER = True
    SECURE_CONTENT_TYPE_NOSNIFF = True
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_SECONDS = 31536000
    SECURE_REDIRECT_EXEMPT = []
    SECURE_SSL_REDIRECT = True
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    X_FRAME_OPTIONS = "DENY"

    # Additional security headers
    SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")


LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
        },
    },
    "root": {
        "handlers": ["console"],
        "level": "WARNING",
    },
    "loggers": {
        "django": {
            "handlers": ["console"],
            "level": os.getenv("DJANGO_LOG_LEVEL", "INFO"),
            "propagate": False,
        },
    },
}
