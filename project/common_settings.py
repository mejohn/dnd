"""
Django settings

For more information on this file, see
https://docs.djangoproject.com/en/2.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.1/ref/settings/
"""

import os
import sys

import environ
from django.contrib.messages import DEFAULT_TAGS
from django.contrib.messages import constants as messages
from django.urls import reverse_lazy

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def path(value):
    # Builds absolute paths relative to BASE_DIR
    return os.path.abspath(os.path.join(BASE_DIR, value))


# Read in environment variables. Default values should be secure.
env = environ.Env(
    DEBUG=(bool, False),
    SECRET_KEY=str,
    GOOGLE_ANALYTICS_KEY=(str, ''),
    SENTRY_DSN=(str, ''),
)
env.read_env(path('.env'))  # parse .env into os.environ

AUTH_USER_MODEL = 'utils.User'

LOGIN_URL = reverse_lazy('login')
LOGOUT_URL = reverse_lazy('logout')

LOGIN_REDIRECT_URL = reverse_lazy('home')
LOGOUT_REDIRECT_URL = reverse_lazy('home')

AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
]

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = env('DEBUG')

SECRET_KEY = env('SECRET_KEY')

# With DEBUG off, Django checks that the Host header in requests matches one of
# these. If you turn off DEBUG and you're suddenly getting HTTP 400 Bad
# Request responses, you need to add the host names to this list
ALLOWED_HOSTS = env.list('ALLOWED_HOSTS')

SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.humanize',
    'django.forms',

    'project.utils',
    'dnd',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'project.urls'

WSGI_APPLICATION = 'project.wsgi.application'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [path('templates'), ],
        'APP_DIRS': True,
        'OPTIONS': {
            'debug': DEBUG,
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'project.utils.context_processors.google_analytics',
            ],
        },
    },
]

# This non-standard form renderer lets us override the templates for
# individual widgets
FORM_RENDERER = 'django.forms.renderers.TemplatesSetting'

# Database settings are pulled from the DATABASE_URL environment variable.
DATABASES = {
    'default': env.db(),
}

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.'
                'UserAttributeSimilarityValidator'
    },
    {
        'NAME': 'django.contrib.auth.password_validation.'
                'MinimumLengthValidator'
    },
    {
        'NAME': 'django.contrib.auth.password_validation.'
                'CommonPasswordValidator'
    },
    {
        'NAME': 'django.contrib.auth.password_validation.'
                'NumericPasswordValidator'
    },
]

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'US/Eastern'

USE_I18N = True

USE_L10N = True

USE_TZ = True

STATIC_URL = '/static/'

STATICFILES_DIRS = [
    path('static')
]

MEDIA_URL = '/media/'

# Messages - tags compatible w/ bootstrap and django admin styles
MESSAGE_TAGS = {
    messages.DEBUG: 'alert-debug %s' % DEFAULT_TAGS[messages.DEBUG],
    messages.INFO: 'alert-info %s' % DEFAULT_TAGS[messages.INFO],
    messages.SUCCESS: 'alert-success %s' % DEFAULT_TAGS[messages.SUCCESS],
    messages.WARNING: 'alert-warning %s' % DEFAULT_TAGS[messages.WARNING],
    messages.ERROR: 'alert-danger %s' % DEFAULT_TAGS[messages.ERROR],
}

# Google Analytics
GOOGLE_ANALYTICS_KEY = env('GOOGLE_ANALYTICS_KEY')

# Sentry/Raven
# To support sentry logging, set the DSN in your .env file. You will need an
# account on a sentry server and create a project to get a DSN.
#
# You will also need to install the "raven" package in your virtualenv
# (remember to add it to your requirements.in)
#
# Installing the raven_compat app will log all Django request handling
# exceptions (500 errors)
#
# You may also wish to install the raven logger to capture logging warnings
# or errors. Simply install a handler with class
# 'raven.contrib.django.raven_compat.handlers.SentryHandler' and configure a
# logger to use it.
#
# See https://docs.sentry.io/clients/python/integrations/django/
if env('SENTRY_DSN'):
    import raven.exceptions

    INSTALLED_APPS.append('raven.contrib.django.raven_compat')

    try:
        with open(path('version'), 'r') as versionfile:
            release = versionfile.read().strip()
    except FileNotFoundError:
        try:
            release = raven.fetch_git_sha(BASE_DIR)
        except raven.exceptions.InvalidGitRepository:
            release = 'unknown'

    RAVEN_CONFIG = {
        'dsn': env('SENTRY_DSN'),
        'release': release,
    }

# Our preferred logging configuration.
# Django takes the LOGGING setting and passes it as-is into Python's
# logging dict-config function (logging.config.dictConfig())
# For information about how Python's logging facilities work, see
# https://docs.python.org/3.5/library/logging.html
#
# The brief 3-paragraph summary is:
# Loggers form a tree hierarchy. A log message is emitted to a logger
# somewhere in this tree, and the hierarchy is used to determine what to do
# with the message.
#
# Each logger may have a level. A message also has a level. A message is
# emitted if its level is greater than its logger's level, or in case its
# logger doesn't have a level, the next one down in the hierarchy (repeat all
# the way until it hits the root, which always has a level). Note that the
# first logger with a level is the ONLY logger whose level is used in this
# decision.
#
# Each logger may have zero or more handlers, which determine what to do with
# a message that is to be emitted (e.g. print it, email it, write to a file). A
# message that passes the level test travels down the hierarchy, being sent
# to each handler at each logger, until it reaches the root logger or a
# logger marked with propagate=False. Each handler may do level checks or
# additional filtering of its own.
#
#
# Typically, you will want to log messages within your application under your
# own logger or a sublogger for each component, often named after the modules,
# such as "myapp.views",  "myapp.models", etc. Then you can customize what to
# do with messages from different components of your app.
#
# You don't need to declare a loggers in the config; they are created
# implicitly with no level and no handlers when calling logging.getLogger()

# This gets whether stderr is attached to a tty. Sometimes stderr may be
# replaced by a file-like object that doesn't have an .isatty() method, e.g.
# when running under Dramatiq. In this particular case, stderr is a file-like
# object that wraps a pipe that sends output to the master process. There's no
# way to detect whether that will ultimately end up at a tty or not, but
# a good guess is to look at the process's original stderr at sys.__stderr__
STDERR_ISATTY = sys.stderr.isatty() if hasattr(sys.stderr, "isatty") else sys.__stderr__.isatty()

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "filters": {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse',
        },
        'require_debug_true': {
            '()': 'django.utils.log.RequireDebugTrue',
        },
    },
    "formatters": {
        "color": {
            "()": "colorlog.ColoredFormatter",
            "format": "%(log_color)s%(levelname)-8s%(reset)s [%(name)s] "
                      "%(message)s",
            "log_colors": {"DEBUG": "cyan",
                           "INFO": "white",
                           "WARNING": "yellow",
                           "ERROR": "red",
                           "CRITICAL": "white,bg_red",
                           }
        },
        "nocolor": {
            "format": "%(asctime)s %(levelname)-8s [%(name)s] "
                      "%(message)s",
            "datefmt": '%Y-%m-%d %H:%M:%S',
        },
    },
    "handlers": {
        "stderr": {
            "class": "logging.StreamHandler",
            "formatter": "color" if STDERR_ISATTY else "nocolor",
        },
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        }
    },
    "loggers": {
        "django": {
            # Django logs everything it does under this handler. We want
            # the level to inherit our root logger level and handlers,
            # but also add a mail-the-admins handler if an error comes to this
            # point (Django sends an ERROR log for unhandled exceptions in
            # views)
            "handlers": ["mail_admins"],
            "level": "NOTSET",
        },
        "django.db": {
            # Set to DEBUG to see all database queries as they happen.
            # Django only sends these messages if settings.DEBUG is True
            "level": "INFO",
        },
        "py.warnings": {
            # This is a built-in Python logger that receives warnings from
            # the warnings module and emits them as WARNING log messages*. By
            # default, this logger prints to stderr. We override that here so
            # that it simply inherits the root logger's handlers
            #
            # * Django enables this behavior by calling
            #   https://docs.python.org/3.5/library/logging.html#logging.captureWarnings
        },
        "appname": {
            "level": "DEBUG" if DEBUG else "INFO",
        },
    },
    "root": {
        "handlers": ["stderr"],
        "level": "INFO" if DEBUG else "WARNING",
    },
}
