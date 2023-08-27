
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = 'django-insecure-glcji%6bkrt97h$=7x+m+xpdhck+fi^v&y-ooug8jto(%pgo$!'

DEBUG = True

ALLOWED_HOSTS = []

#This tells Django which apps are part of the project
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'find_a_volunteer_dir',
    'users',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'find_a_volunteer.urls'

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
            ],
        },
    },
]

WSGI_APPLICATION = 'find_a_volunteer.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

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

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True

STATIC_URL = 'static/'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

AUTH_USER_MODEL= 'users.CustomUser' #This tells Django to use my CustomUserModel instead of the default one

#The section below tells Django where to find the templates that I use.
import os
SETTINGS_PATH = os.path.dirname(os.path.dirname(__file__))
TEMPLATE_DIRS = (
    os.path.join(SETTINGS_PATH, 'templates'),
)

#The line below tells Django which URL to redirect users to after they logout.
LOGOUT_REDIRECT_URL = '/'

#Django cannot save media files to everywhere on the host machine. To be able to save media...
#...files to a certain directory, I need to tell Django that that certain directory is where...
#...media files belong to be saved to. Below, I tell Django that the "user_images" directory is where media...
#...files belong to be saved to.
MEDIA_URL = '/user_images/'
MEDIA_ROOT = 'C:/Users/arunh/Python NEA/find_a_volunteer/user_images/'

#The below is used to tell Django where to look when a template loads/collects the static files.
#Static files are files stored on the web hosting machine which need to be sent to the browser when requested.
STATICFILES_DIRS = [ 
    'C:/Users/arunh/Python NEA/find_a_volunteer/user_images/'
]
