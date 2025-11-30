import os
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SECRET_KEY = 'dev-key'
DEBUG = True
ALLOWED_HOSTS = ['*']
INSTALLED_APPS = [
    'django.contrib.contenttypes',
    'django.contrib.staticfiles',
    'tasks',
]
MIDDLEWARE = ['django.middleware.common.CommonMiddleware']
ROOT_URLCONF = 'backend.urls'
TEMPLATES = []
WSGI_APPLICATION = 'backend.wsgi.application'
DATABASES = {'default': {'ENGINE': 'django.db.backends.sqlite3','NAME': os.path.join(BASE_DIR, 'db.sqlite3')}}
STATIC_URL = '/static/'
STATICFILES_DIRS = [os.path.join(BASE_DIR, '..', 'frontend')]
