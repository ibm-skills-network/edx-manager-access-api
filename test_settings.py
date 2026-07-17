"""
These settings are here to use during tests, because django requires them.
In a real-world use case, apps in this project are installed into other
Django applications, so these settings will not be used.
"""

from os.path import abspath, dirname, join


def root(*args):
    """
    Get the absolute path of the given path relative to the project root.
    """
    return join(abspath(dirname(__file__)), *args)


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'default.db',
        'USER': '',
        'PASSWORD': '',
        'HOST': '',
        'PORT': '',
    }
}

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'rest_framework',
    'edx_manager_access_api',
)

LOCALE_PATHS = [
    root('edx_manager_access_api', 'conf', 'locale'),
]

ROOT_URLCONF = 'edx_manager_access_api.urls'

SECRET_KEY = 'insecure-secret-key'
BASICAUTH_DISABLE = True

# Username of the dedicated service account allowed to call the
# manager-access grant/revoke endpoints (see IsServiceAccount permission).
AUTH_USERNAME = 'sn-service'
