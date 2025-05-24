
from pathlib import Path
from dotenv import load_dotenv
import os
import logging
logger = logging.getLogger('django')
from django.http import HttpResponseServerError
import logging.handlers
from logging.handlers import TimedRotatingFileHandler
BASE_DIR = Path(__file__).resolve().parent.parent.parent
from datetime import timedelta




DEBUG=False

ALLOWED_HOSTS = ["*"]
#  ['demosurvey.pythonanywhere.com']


SECRET_KEY = 'django-insecure-kl#lbep#5wde!b$7odnwta*t$sl18$k041&)+%z5yvey4l=j!h'



DATABASES = {
    'default': {

        'ENGINE': 'django.db.backends.mysql',
        'NAME': "demosurvey$django_survey_db",
        'USER': 'demosurvey',
        'PASSWORD': 'admin1899',
        'HOST': "demosurvey.mysql.pythonanywhere-services.com",
        'PORT': '3306',

    }
}








LOGIN_URL = '/login/'
LOGIN_REDIRECT_URL =  '/'
LOGOUT_REDIRECT_URL = '/login/'


RECORD_PER_PAGE = 10

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

AUTH_USER_MODEL = "survey_app.CustomUser"
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATIC_URL = 'static/'
ROOT_URLCONF = 'core.urls'

USE_TZ = True
USE_I18N = False
TIME_ZONE = 'UTC'

LANGUAGE_CODE = 'en-us'
STATIC_URL = 'static/'




INSTALLED_APPS = [
      "whitenoise.runserver_nostatic",

    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
            'debug_toolbar',
      'rest_framework',
    "survey_app",

]








MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
     'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
        'django_auto_logout.middleware.auto_logout',
        'debug_toolbar.middleware.DebugToolbarMiddleware',
            'survey_app.middleware.TimezoneMiddleware',
        # 'survey_app.middleware.ExceptionLoggingMiddleware',
            'survey_app.middleware.LoginRequiredMiddleware',

]



AUTO_LOGOUT = {
    'IDLE_TIME': timedelta(days=7),
    'REDIRECT_TO_LOGIN_IMMEDIATELY': True,
        'MESSAGE': 'The session has expired. Please login again to continue.',
}


REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
    'rest_framework.authentication.SessionAuthentication',
    ),
        'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ]
}






TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                  'django_auto_logout.context_processors.auto_logout_client',
                     'survey_app.context_processors.dynamic_model_name',  # Add this line

            ],
        },
    },
]

WSGI_APPLICATION = 'core.wsgi.application'




AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    # {
    #     'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    # },
    # {
    #     'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    # },
]
STORAGES = {
    "default": {
        "BACKEND": "django.core.files.storage.FileSystemStorage",
    },

    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
    },
}


DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


log_dir = 'logs'
if not os.path.exists(log_dir):
    os.makedirs(log_dir)

# LOGGING = {
#     'version': 1,
#     'disable_existing_loggers': False,
#     'formatters': {
#         'verbose': {
#             'format': '{levelname} {asctime} {module} {message} {exc_info}',
#             'style': '{',
#         },
#         'simple': {
#             'format': '{levelname} {message}',
#             'style': '{',
#         },
#     },
#     'handlers': {
#         'file_error': {
#             'level': 'ERROR',
#             'class': 'logging.handlers.TimedRotatingFileHandler',
#             'filename': os.path.join(log_dir, 'errors.log'),
#             'when': 'midnight',  # Rotate at midnight
#             'backupCount': 10,    # Keep at most 10 log files
#             'formatter': 'verbose',
#         },
#         'file_warning': {
#             'level': 'WARNING',
#             'class': 'logging.handlers.TimedRotatingFileHandler',
#             'filename': os.path.join(log_dir, 'warnings.log'),
#             'when': 'midnight',  # Rotate at midnight
#             'backupCount': 10,    # Keep at most 10 log files
#             'formatter': 'verbose',
#         },
#         'file_all': {
#             'level': 'INFO',
#             'class': 'logging.handlers.TimedRotatingFileHandler',
#             'filename': os.path.join(log_dir, 'all.log'),
#             'when': 'midnight',  # Rotate at midnight
#             'backupCount': 10,    # Keep at most 10 log files
#             'formatter': 'verbose',
#         },
#     },
#     'loggers': {
#         'django': {
#         # '': {  # To collect loginng from all apps
#             'handlers': ['file_error', 'file_warning', 'file_all'],
#             'level': 'DEBUG',
#             'propagate': True,
#         },
#     },
# }


























# for show debug_toolbar in nmormal pages
INTERNAL_IPS = [
    '127.0.0.1',
]

