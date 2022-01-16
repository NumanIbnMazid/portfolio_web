from .base import *

# ----------------------------------------------------
# *** Allowed Hosts ***
# ----------------------------------------------------

ALLOWED_HOSTS = ["mysite.example.com"]

# ----------------------------------------------------
# *** Databases ***
# ----------------------------------------------------

DATABASES = {'default': get_env_value('DATABASE_URL')}
# set atomic requests
# DATABASES["default"]["ATOMIC_REQUESTS"] = True
DATABASES["default"]["CONN_MAX_AGE"] = env.int("CONN_MAX_AGE", default=60)

# ----------------------------------------------------
# *** Debug ***
# ----------------------------------------------------

DEBUG = False

# ----------------------------------------------------
# *** Templates ***
# ----------------------------------------------------

TEMPLATES[0]["DIRS"] = [os.path.join(root.path(), "templates")]

# ----------------------------------------------------
# *** LOGGING ***
# ----------------------------------------------------

# https://docs.djangoproject.com/en/dev/ref/settings/#logging
# See https://docs.djangoproject.com/en/dev/topics/logging for more details on how to customize logging configuration.

LOGGING = {
    "version": 1,
    "disable_existing_loggers": True,
    "formatters": {
        "verbose": {
            "format": "%(levelname)s %(asctime)s %(module)s "
            "%(process)d %(thread)d %(message)s"
        }
    },
    "handlers": {
        "console": {
            "level": "DEBUG",
            "class": "logging.StreamHandler",
            "formatter": "verbose",
        }
    },
    "root": {"level": "INFO", "handlers": ["console"]},
    "loggers": {
        "django.db.backends": {
            "level": "ERROR",
            "handlers": ["console"],
            "propagate": False,
        },
        # Errors logged by the SDK itself
        "sentry_sdk": {"level": "ERROR", "handlers": ["console"], "propagate": False},
        "django.security.DisallowedHost": {
            "level": "ERROR",
            "handlers": ["console"],
            "propagate": False,
        },
    },
}

# ----------------------------------------------------
# *** Others ***
# ----------------------------------------------------

# ADMIN
# ------------------------------------------------------------------------------
# Django Admin URL regex.
ADMIN_URL = env.str("DJANGO_ADMIN_URL")

# ==============================================================================
# *** SECURITY SETTINGS ***
# ==============================================================================

# https://docs.djangoproject.com/en/dev/ref/settings/#secure-proxy-ssl-header
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
# https://docs.djangoproject.com/en/dev/ref/settings/#secure-ssl-redirect
SECURE_SSL_REDIRECT = env.bool("DJANGO_SECURE_SSL_REDIRECT", default=True)
# https://docs.djangoproject.com/en/dev/ref/settings/#session-cookie-secure
SESSION_COOKIE_SECURE = True
# https://docs.djangoproject.com/en/dev/ref/settings/#csrf-cookie-secure
CSRF_COOKIE_SECURE = True
# https://docs.djangoproject.com/en/dev/topics/security/#ssl-https
# https://docs.djangoproject.com/en/dev/ref/settings/#secure-hsts-seconds
# TODO: set this to 60 seconds first and then to 518400 once you prove the former works
SECURE_HSTS_SECONDS = 60 # 60 * 60 * 24 * 7 * 52  # one year
# https://docs.djangoproject.com/en/dev/ref/settings/#secure-hsts-include-subdomains
SECURE_HSTS_INCLUDE_SUBDOMAINS = env.bool(
    "DJANGO_SECURE_HSTS_INCLUDE_SUBDOMAINS", default=True
)
# https://docs.djangoproject.com/en/dev/ref/settings/#secure-hsts-preload
SECURE_HSTS_PRELOAD = env.bool("DJANGO_SECURE_HSTS_PRELOAD", default=True)
# https://docs.djangoproject.com/en/dev/ref/middleware/#x-content-type-options-nosniff
SECURE_CONTENT_TYPE_NOSNIFF = env.bool(
    "DJANGO_SECURE_CONTENT_TYPE_NOSNIFF", default=True
)
CSRF_COOKIE_HTTPONLY = True
SECURE_BROWSER_XSS_FILTER = True


# ----------------------------------------------------
# *** --------------- Third Party --------------- ***
# ----------------------------------------------------

# ----------------------------------------------------
# *** Django Cors Headers ***
# ----------------------------------------------------

CORS_ORIGIN_ALLOW_ALL = False

CORS_ORIGIN_WHITELIST = (
    'http://mysite.example.com',
)

# ----------------------------------------------------
# *** Django Compressor ***
# ----------------------------------------------------

# https://django-compressor.readthedocs.io/en/stable/settings.html?highlight=COMPRESS_ENABLED#django.conf.settings.COMPRESS_ENABLED
COMPRESS_ENABLED = env.bool("COMPRESS_ENABLED", default=True)
# https://django-compressor.readthedocs.io/en/stable/settings.html?highlight=COMPRESS_URL#django.conf.settings.COMPRESS_URL
COMPRESS_URL = STATIC_URL
# https://django-compressor.readthedocs.io/en/stable/settings.html?highlight=COMPRESS_OFFLINE#django.conf.settings.COMPRESS_OFFLINE
COMPRESS_OFFLINE = True  # Offline compression is required when using Whitenoise
# https://django-compressor.readthedocs.io/en/stable/settings.html?highlight=COMPRESS_OFFLINE#django.conf.settings.COMPRESS_OFFLINE_TIMEOUT
COMPRESS_OFFLINE_TIMEOUT = 31536000 # 1 year
# https://django-compressor.readthedocs.io/en/stable/settings.html?highlight=COMPRESS_FILTERS#django.conf.settings.COMPRESS_FILTERS
COMPRESS_FILTERS = {
    "css": [
        "compressor.filters.css_default.CssAbsoluteFilter",
        "compressor.filters.cssmin.rCSSMinFilter",
    ],
    "js": ["compressor.filters.jsmin.JSMinFilter"],
}
