
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
load_dotenv()

USER_DEFAULT_PERMISSIONS = {
  
    "survey_access": True,
    "settings_access": False,
}


LOGIN_URL = '/login/'
LOGIN_REDIRECT_URL =  '/'
LOGOUT_REDIRECT_URL = '/login/'

APPEND_SLASH=False #prevent  url error when user dont add / at end of url
RECORD_PER_PAGE = 50

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'  

AUTH_USER_MODEL = "survey_app.CustomUser"
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATIC_URL = 'static/'
ROOT_URLCONF = 'core.urls'


USE_TZ = True
USE_I18N = False
TIME_ZONE = 'UTC'  

SESSION_COOKIE_AGE = 3 * 24 * 60 * 60   # Session expires after 3 days

STATIC_URL = 'static/'


# Default language for the project (English)
LANGUAGE_CODE = 'en'  
LANG = 'en_US.UTF-8'  # English (United States) locale with UTF-8 encoding
DEFAULT_CHARSET = 'utf-8'  # Default character encoding for the project
FILE_CHARSET = 'utf-8'  # Character encoding for file operations


 # Default language for the project (AR)
# LANGUAGE_CODE = 'ar' 
# LANG = 'ar_SA.UTF-8'  # Arabic locale (ensure it's installed on your system)
# DEFAULT_CHARSET = 'utf-8'  # Default character encoding for the project
# FILE_CHARSET = 'utf-8'  # Character encoding for file operations




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
            'survey_app.middleware.CheckLoginStateMiddleware',
            'survey_app.middleware.TimezoneMiddleware',
        'survey_app.middleware.ExceptionLoggingMiddleware',  
            'survey_app.middleware.LoginRequiredMiddleware', # this redirect request to login if not logged in

]



AUTO_LOGOUT = {
    'IDLE_TIME': timedelta(days=5),
    'REDIRECT_TO_LOGIN_IMMEDIATELY': True,
        'MESSAGE': 'The session has expired. Please login again to continue.',
}


REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
                # 'rest_framework_simplejwt.authentication.JWTAuthentication',   
                        'rest_framework.authentication.SessionAuthentication', # to remove after test
        ),
        'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated', 
    ],
        # global  exception handler to avoid repeting try catch blocks
        'EXCEPTION_HANDLER': 'survey_app.exception_handler.custom_exception_handler', 
}









SIMPLE_JWT = {
    # "ACCESS_TOKEN_LIFETIME": timedelta(minutes=15),
    "ACCESS_TOKEN_LIFETIME": timedelta(days=1),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=3),
  
    "ALGORITHM": "HS256",
    "SIGNING_KEY": os.getenv('SECRET_KEY'),
    
    
    
    #  requires the Blacklist App to work!
#  "ROTATE_REFRESH_TOKENS": True , 
        # 'BLACKLIST_AFTER_ROTATION': True,
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
                     'survey_app.context_processors.dynamic_model_name',  
                     'survey_app.context_processors.is_role_admin_fun_from_context',  
                     
                
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

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {message} {exc_info}',
            'style': '{',
        },
        'simple': {
            'format': '{levelname} {message}',
            'style': '{',
        },
    },
    'handlers': {
        'file_error': {
            'level': 'ERROR',
            'class': 'logging.handlers.TimedRotatingFileHandler',
            'filename': os.path.join(log_dir, 'errors.log'),
            'when': 'midnight',  # Rotate at midnight
            'backupCount': 10,    # Keep at most 10 log files
            'formatter': 'verbose',
        },
        'file_warning': {
            'level': 'WARNING',
            'class': 'logging.handlers.TimedRotatingFileHandler',
            'filename': os.path.join(log_dir, 'warnings.log'),
            'when': 'midnight',  # Rotate at midnight
            'backupCount': 10,    # Keep at most 10 log files
            'formatter': 'verbose',
        },
        'file_all': {
            'level': 'INFO',
            'class': 'logging.handlers.TimedRotatingFileHandler',
            'filename': os.path.join(log_dir, 'all.log'),
            'when': 'midnight',  # Rotate at midnight
            'backupCount': 10,    # Keep at most 10 log files
            'formatter': 'verbose',
        },
    },
    'loggers': {
        'django': {
        # '': {  # To collect loginng from all apps
            'handlers': ['file_error', 'file_warning', 'file_all'],
            'level': 'DEBUG',
            'propagate': True,
        },
    },
}

