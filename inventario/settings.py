"""
Django settings for inventario project.

Generated by 'django-admin startproject' using Django 3.2.3.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.2/ref/settings/
"""

from pathlib import Path
import os

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-(nb%(5amp0x8l+4q$$(b#yipxamb_lr%$(k%5&e!owocy*&ij$'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'inventarioTienda',
    'menuAndWelcome',
    'log_viewer',
    'dbbackup',  
]

DBBACKUP_STORAGE = 'django.core.files.storage.FileSystemStorage'
DBBACKUP_STORAGE_OPTIONS = {'location': '/var/backup/dir/'}

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'inventario.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR,"templates")],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'inventario.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# Password validation
# https://docs.djangoproject.com/en/3.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/3.2/topics/i18n/

LANGUAGE_CODE = 'es'

TIME_ZONE = 'America/Lima'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/

STATIC_URL = '/static/'


#... https://docs.djangoproject.com/en/3.2/ref/settings/#std:setting-STATICFILES_DIRS
STATICFILES_DIRS = [
    BASE_DIR / "static", 
]

STATIC_ROOT = os.path.join(BASE_DIR, 'public')
# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

LOGIN_REDIRECT_URL = "inicio"
LOGOUT_REDIRECT_URL = "inicio"

#https://docs.sentry.io/platforms/python/guides/django/
""" import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration

sentry_sdk.init(
    dsn="https://7f8760b7af064d5c99c8b7ad2186f541@o1388441.ingest.sentry.io/6710803",
    integrations=[
        DjangoIntegration(),
    ],

    # Set traces_sample_rate to 1.0 to capture 100%
    # of transactions for performance monitoring.
    # We recommend adjusting this value in production.
    traces_sample_rate=1.0,

    # If you wish to associate users to errors (assuming you are using
    # django.contrib.auth) you may enable sending PII data.
    send_default_pii=True
) """

#comandos fre https://pypi.org/project/django-log-viewer/
#https://github.com/agusmakmun/django-log-viewer
#configura los logs de manera que aparezca el pattern primero

LOG_VIEWER_FILES = ['logfile1', 'logfile2', ...]
LOG_VIEWER_FILES_PATTERN = '*.log*'
LOG_VIEWER_FILES_DIR = '/var/log/'
LOG_VIEWER_PAGE_LENGTH = 25       # total log lines per-page
LOG_VIEWER_MAX_READ_LINES = 1000  # total log lines will be read
LOG_VIEWER_FILE_LIST_MAX_ITEMS_PER_PAGE = 25 # Max log files loaded in Datatable per page
LOG_VIEWER_PATTERNS = ['[INFO]', '[DEBUG]', '[WARNING]', '[ERROR]', '[CRITICAL]']
LOG_VIEWER_EXCLUDE_TEXT_PATTERN = None  # String regex expression to exclude the log from line

PRODUCTION = True
if PRODUCTION:
    from inventario.prod import *  # or specific overrides

#PARA PROD:
#usando pyinstaller
""" 
    Antes que nada es necesario tener el debug en true para saber donde deben ir nuestros
    archivos estaticos y templates
    para los archivos estaticos se debe hacer collecstatic en el proyecto django
    para que se generen en una carpeta de static root en nuestro caso public 
    esta carpeta se mueve solo con los archivos estaticos que usamos en el proyecto no 
    los por defecto de django

    para los templates debemos crear una carpeta templates donde dentro pongamos todas las
    subcarpetas que estan en nuestros templates originales, respetando la estructura de carpetas

    una vez con esto debemos irnos a la carpeta raiz de nuestro proyecto original
    usaremos pyi-makespec --onedir manage.py esto nos genera un archivo .spec 
    no lo tocamos aun y hacemos pyinstaller .spec esto nos genera una carpeta dist
    dentro estara el ejecutable lo ejecutamos con manage.exe runserver --noreload
    si tenemos debug activado veremos que faltan lso archivos staticos y templates
    debemos mover las dos carpetas que tenemos

    Ahora deberiamos comprobar que no nos olvidamos de nada, y en caso de contar con 
    una extension en mi caso yo usaba log viewer.py debemos ir a el url que usa ese template o static
    nos saldra un error de faltante, debemos ir donde tenemos esos archivos en mi caso
    estaba usando virtualenv y en la carpeta de Lib/site-packages/log_viewer/templates tenia lso templates y 
    en Lib/site-packages/log_viewer/static tenia los archivos estaticos, debemos copiarlos a las  carpetas
    correspondientes.

    Con esto tenemos una carpeta lista para distribuir, si queremos tenerlo todo en un solo archivo debemos hacer 
    unos pasos mas esta vez hacemos una copia de nuestro manage.spec y hacemos pyi-makespec --onefile manage.py
    este nuevo archivo tenemos que añadir en a.datas[] las direcciones de las carpetas creadas

    algo asi: (windows)
"""
# datas=[
#        ('C:\\Users\\Usuario\\Desktop\\manage\\templates', 'templates'), 
#        ('C:\\Users\\Usuario\\Desktop\\manage\\public', 'public'), 
# ],
"""
    hecho esto podemos hacer pyinstaller .spec y tendriamos un solo archivo ejecutable.
"""

    




#primero se hace collecstatic de manage.py
#hacemos un pyi-makespec --onefile yourprogram.py   si queremos mas opciones se añade
#luego segun la distribucion de nuestro proyecto ordenamos la carpeta generada
#si no generamos un spec sin onefile y lo instalamos, antes configurando el spec con el nombre del programa
# con pyinstaller .spec
#esperamos y una vez terminado hacemos .exe collecstatic esto nos dara errores
#guiandonos en como deberia estar distribuido nuestra carpeta
#una vez tenemos la distribucion correcta nos vamos al archivo  .spec y configuramos
#el diccionario data con el origen y destino segun la distribucion correcta
#hacemos lo mismo para templates
#volvemos a generar el archivo y testeamos que funcione correctamente
#./dist/manage/manage runserver --noreload