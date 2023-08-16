from A.settings import *


SECRET_KEY = 'django-insecure-58&ie02a=c-*xa_k0!n6++@*#=t+$^(b0ieo12lb^id18uy8#d'
DEBUG = True

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'django.contrib.humanize',
    'django.contrib.sites',
    'django.contrib.sitemaps',

    # installed apps
    'projects.apps.ProjectsConfig',
    'accounts.apps.AccountsConfig',

    # thirdparty apps
    'django_extensions',

]

SITE_ID = 2

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

STATICFILES_DIRS = [BASE_DIR / 'static']

MEDIA_ROOT = BASE_DIR / 'static/images'
STATIC_ROOT = BASE_DIR / 'staticfiles'
