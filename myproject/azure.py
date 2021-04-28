import os
from storages.backends.azure_storage import AzureStorage

ALLOWED_HOSTS = [os.environ['WEBSITE_HOSTNAME']] if 'WEBSITE_HOSTNAME' in os.environ else []

hostname = os.environ['DBHOST']
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ['DBNAME'],
        'HOST': os.environ['DBHOST'],
        'USER': os.environ['DBUSER'] + "@" + hostname,
        'PASSWORD': os.environ['DBPASS'] 
    }
}
SECRET_KEY = os.getenv('SECRET_KEY')
DEBUG = os.environ.get('DEBUG')

AZURE_ACCOUNT_NAME = os.environ['AZURE_ACCOUNT_NAME']
AZURE_STORAGE_KEY = os.environ['AZURE_STORAGE_KEY']
AZURE_MEDIA_CONTAINER = os.environ['AZURE_MEDIA_CONTAINER']
AZURE_STATIC_CONTAINER = os.environ['AZURE_STATIC_CONTAINER']

class AzureStaticStorage(AzureStorage):
    account_name = AZURE_ACCOUNT_NAME
    account_key = AZURE_STORAGE_KEY
    azure_container = 'static'
    expiration_secs = None

class AzureMediaStorage(AzureStorage):
    account_name = AZURE_ACCOUNT_NAME
    account_key = AZURE_STORAGE_KEY
    azure_container = 'media'
    expiration_secs = None


DEFAULT_FILE_STORAGE = 'AzureMediaStorage'
STATICFILES_STORAGE = 'AzureStaticStorage'
AZURE_CUSTOM_DOMAIN = f'{AZURE_ACCOUNT_NAME}.blob.core.windows.net'
STATIC_URL = f'https://{AZURE_CUSTOM_DOMAIN}/{AZURE_STATIC_CONTAINER}'
MEDIA_URL = f'https://{AZURE_CUSTOM_DOMAIN}/{AZURE_MEDIA_CONTAINER}'
