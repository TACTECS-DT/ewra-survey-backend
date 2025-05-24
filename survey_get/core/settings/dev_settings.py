from .common import *
import os
from dotenv import load_dotenv
load_dotenv()


ENV_SECRET_KEY =  os.getenv('SECRET_KEY')
DATABASE_ENGINE =  os.getenv('DATABASE_ENGINE')
DATABASE_NAME =  os.getenv('DATABASE_NAME')
DATABASE_USER =  os.getenv('DATABASE_USER')
DATABASE_PASSWORD =  os.getenv('DATABASE_PASSWORD')
DATABASE_HOST =  os.getenv('DATABASE_HOST')
DATABASE_PORT =  os.getenv('DATABASE_PORT')

SECRET_KEY = ENV_SECRET_KEY

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'


DEBUG=False
ALLOWED_HOSTS = ["*"]

DATABASES = {
    'default': {
        
        'ENGINE': DATABASE_ENGINE,
        'NAME': DATABASE_NAME,
        'USER': DATABASE_USER,
        'PASSWORD': DATABASE_PASSWORD,
        'HOST': DATABASE_HOST,  
        'PORT': DATABASE_PORT,  
            
    }
}


# SECURE_SSL_REDIRECT = False
# SECURE_BROWSER_XSS_FILTER = False
# SECURE_CONTENT_TYPE_NOSNIFF = False
# SESSION_COOKIE_SECURE = False
# CSRF_COOKIE_SECURE = False
# SECURE_HSTS_SECONDS = 0

# SECURE_HSTS_PRELOAD = False
# SECURE_HSTS_INCLUDE_SUBDOMAINS = False 
 







# for show debug_toolbar in nmormal pages 
INTERNAL_IPS = [
    '127.0.0.1',  
]

