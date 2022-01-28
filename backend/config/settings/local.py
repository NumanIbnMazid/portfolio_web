from .base import *

# ----------------------------------------------------
# *** Allowed Hosts ***
# ----------------------------------------------------

ALLOWED_HOSTS = ['*']

# ----------------------------------------------------
# *** Databases ***
# ----------------------------------------------------

if os.environ.get('GITHUB_WORKFLOW'):
    DATABASES = {
        'default': {
           'ENGINE': 'django.db.backends.postgresql',
           'NAME': 'github_actions',
           'USER': 'postgres',
           'PASSWORD': 'postgres',
           'HOST': '127.0.0.1',
           'PORT': '5432',
        }
    }

elif os.environ.get('DATABASE_URL') is not None:
    DATABASES = {'default': env.db('DATABASE_URL')}

else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': os.path.join(BASE_DIR , 'project.db.sqlite3'),
        }
    }

# remove sslmode for local development
options = DATABASES['default'].get('OPTIONS', {})
options.pop('sslmode', None)
# set atomic requests
# DATABASES["default"]["ATOMIC_REQUESTS"] = True

# ----------------------------------------------------
# *** Debug ***
# ----------------------------------------------------

DEBUG = True

# ----------------------------------------------------
# *** Templates ***
# ----------------------------------------------------

TEMPLATES[0]["DIRS"] = [os.path.join(root.path(), "templates")]

# ----------------------------------------------------
# *** CACHES ***
# ----------------------------------------------------

# https://docs.djangoproject.com/en/dev/ref/settings/#caches

CACHES = {
    'default': {
        'BACKEND': 'djpymemcache.backend.PyMemcacheCache', # https://github.com/django-pymemcache/django-pymemcache
        'LOCATION': '127.0.0.1:11211',
    },
    'rosetta': {
        'BACKEND': 'djpymemcache.backend.PyMemcacheCache', # https://github.com/django-pymemcache/django-pymemcache
        'LOCATION': '127.0.0.1:11211',
    }
}

# ----------------------------------------------------
# *** LOGGING ***
# ----------------------------------------------------

# https://docs.djangoproject.com/en/dev/ref/settings/#logging
# See https://docs.djangoproject.com/en/dev/topics/logging for more details on how to customize logging configuration.

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
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
    "root": {
        "level": "INFO",
        "handlers": ["console"]
    }
}


# ----------------------------------------------------
# *** --------------- Third Party --------------- ***
# ----------------------------------------------------

# ----------------------------------------------------
# *** Django Cors Headers ***
# ----------------------------------------------------

CORS_ORIGIN_ALLOW_ALL = True

# ----------------------------------------------------
# *** Django Debug Toolbar ***
# ----------------------------------------------------

if not "debug_toolbar" in INSTALLED_APPS:
    INSTALLED_APPS += ["debug_toolbar"]

if not "debug_toolbar.middleware.DebugToolbarMiddleware" in MIDDLEWARE:
    MIDDLEWARE += ["debug_toolbar.middleware.DebugToolbarMiddleware"]

# https://django-debug-toolbar.readthedocs.io/en/latest/configuration.html#debug-toolbar-config
DEBUG_TOOLBAR_CONFIG = {
    "DISABLE_PANELS": ["debug_toolbar.panels.redirects.RedirectsPanel"],
    "SHOW_TEMPLATE_CONTEXT": True,
}

INTERNAL_IPS = [
    "127.0.0.1", "0.0.0.0", "10.0.2.2"
]

if env.str("USE_DOCKER", default="no") == "yes":
    import socket

    hostname, _, ips = socket.gethostbyname_ex(socket.gethostname())
    INTERNAL_IPS += [".".join(ip.split(".")[:-1] + ["1"]) for ip in ips]
    try:
        _, _, ips = socket.gethostbyname_ex("node")
        INTERNAL_IPS.extend(ips)
    except socket.gaierror:
        # The node container isn't started (yet?)
        pass
