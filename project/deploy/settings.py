"""
-*- Production Settings -*-

This file contains production-specific settings. Complete the deployment
checklist and make any necessary changes.

https://docs.djangoproject.com/en/1.11/howto/deployment/checklist/
"""

from ..common_settings import *  # noqa: F401,F403
from ..common_settings import env, path


# When DEBUG is off (ie, for production), these email addresses will receive
# an email for any unhandled exceptions while processing a request. See the
# logging configuration in common_settings for how that is set up.
ADMINS = [
    # ('Admin Name', 'admin.email@example.com'),
]

# Some security features that we want to ensure we use during production
# deployments. You can set DISABLE_SSL temporarily when setting things
# up if you need but don't leave it on for production!
ssl_on = not env.bool("DISABLE_SSL", False)
SECURE_SSL_REDIRECT = ssl_on
SESSION_COOKIE_SECURE = ssl_on
CSRF_COOKIE_SECURE = ssl_on


# Django's development server will automatically serve static files for you,
# but in production, Django expects your web server to take care of that. You
# will need to set STATIC_ROOT to a directory on your filesystem, and
# STATIC_URL to something like "/static/". Then configure your webserver to
# serve that directory at that url.
# Finally, run "manage.py collectstatic" and django will copy static files
# from various places into your STATIC_ROOT. You need to re-run collectstatic
# each time you redeploy with changes to static files.
STATIC_ROOT = path(env.str("STATIC_ROOT"))

# manifest storage is useful for its automatic cache busting properties
STATICFILES_STORAGE = 'django.contrib.staticfiles.storage' \
                      '.ManifestStaticFilesStorage'


# Set your MEDIA_ROOT to some directory that's writable by your web server if
# your app involves writing to the filesystem using the default storage class
MEDIA_ROOT = path(env("MEDIA_ROOT"))
