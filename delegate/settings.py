
DEBUG = True
TEMPLATE_DEBUG = DEBUG

ADMINS = ()
MANAGERS = ADMINS

import tempfile, os, hashlib, datetime
from django import contrib
tempdata = tempfile.mkdtemp()
approot = os.path.dirname(os.path.abspath(__file__))
adminroot = os.path.join(contrib.__path__[0], 'admin')

DATABASES = {
    'default': {
        'NAME': os.path.join(tempdata, 'delegate-test.db'),
        'TEST_NAME': os.path.join(tempdata, 'delegate-test.db'),
        'ENGINE': 'django.db.backends.sqlite3',
        'USER': '',
        'PASSWORD': '',
    }
}

TIME_ZONE = 'America/New_York'
LANGUAGE_CODE = 'en-us'
SITE_ID = 1
USE_I18N = False
MEDIA_ROOT = os.path.join(tempdata, 'static')
MEDIA_URL = '/face/'
STATIC_ROOT = os.path.join(tempdata, 'static', 'admin')[0]
STATIC_URL = '/staticfiles/'
ADMIN_MEDIA_PREFIX = '/admin-media/'
SECRET_KEY = hashlib.sha1(
    datetime.datetime.now().isoformat()).hexdigest()

TEMPLATE_DIRS = (
    os.path.join(approot, 'templates'),
    os.path.join(adminroot, 'templates'),
    os.path.join(adminroot, 'templates', 'admin'),
)

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
    'django.template.loaders.eggs.Loader',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.gzip.GZipMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
)

TEMPLATE_CONTEXT_PROCESSORS = (
    "django.contrib.auth.context_processors.auth",
    "django.core.context_processors.request",
    "django.core.context_processors.debug",
    "django.core.context_processors.media",
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.staticfiles',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.admin',
    'delegate',
)

# Logging Configuration
LOGGING = dict(
    version=1,
    disable_existing_loggers=False,
    formatters={
        'standard': {
            'format':
                '%(asctime)s [%(levelname)s] %(name)s: %(message)s' }, },
    handlers={
        'default': {
            'level':'DEBUG',
            'class':'logging.StreamHandler',
            'formatter':'standard' },
        'nil': {
            'level':'DEBUG',
            'class':'django.utils.log.NullHandler', },
    },
    loggers={
        'delegate': { 
            'handlers': ['default'], 
            'level': 'DEBUG', 
            'propagate': False },
    },
)
