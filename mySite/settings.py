"""
Django settings for mySite project.

Generated by 'django-admin startproject' using Django 3.2.19.

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
SECRET_KEY = 'django-insecure-w##_0m9jhd5v3i@nuj9rk^h8*gmrhz+5kys6og@znk_gx1=tve'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# ALLOWED_HOSTS = []
ALLOWED_HOSTS = ALLOWED_HOSTS = ['xxx.xxx.xxx.xxx', '127.0.0.1', 'mysite.com','www.mysite.com']
# ALLOWED_HOSTS = []
SITE_ID = 1


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'blog',
    'taggit',
    'images',
    'django.contrib.sites',
    'django.contrib.sitemaps',
    'django.contrib.postgres',
    'crispy_forms',
    'social_django',
    'django_extensions',
    'bootstrapform',
]
CRISPY_TEMPLATE_PACK = 'bootstrap4'

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django_auto_logout.middleware.auto_logout',
]


ROOT_URLCONF = 'mySite.urls'

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

WSGI_APPLICATION = 'mySite.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases

DATABASES = {
    'default': {
        # 'ENGINE': 'django.db.backends.sqlite3',
        # 'NAME': BASE_DIR / 'db.sqlite3',
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'post',
        'USER': 'postgres',
        'PASSWORD': 'root',
        'PORT': 5432

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

# PASSWORD_HASHERS = [
#     'django.contrib.auth.hashers.PBKDF2PasswordHasher',
#     'django.contrib.auth.hashers.PBKDF2SHA1PasswordHasher',
#     'django.contrib.auth.hashers.Argon2PasswordHasher',
#     'django.contrib.auth.hashers.BCryptSHA256PasswordHasher',
#     'django.contrib.auth.hashers.BCryptPasswordHasher',
#     'django.contrib.auth.hashers.ScryptPasswordHasher',
#     'django.contrib.auth.hashers.SHA1PasswordHasher',
#     'django.contrib.auth.hashers.MD5PasswordHasher',
#     'django.contrib.auth.hashers.UnsaltedSHA1PasswordHasher',
#     'django.contrib.auth.hashers.UnsaltedMD5PasswordHasher',

# ]
# Internationalization
# https://docs.djangoproject.com/en/3.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/

STATIC_URL = '/static/'
MEDIA_URL = 'media/'
MEDIA_ROOT = BASE_DIR/'media'

# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'





EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'

EMAIL_HOST = "smtp.gmail.com"
EMAIL_HOST_USER = "snchorsiya008@gmail.com"
EMAIL_HOST_PASSWORD = "ssfswlboxdhxrbuq"
EMAIL_PORT = 587
EMAIL_USE_TLS = True
DEFAULT_FROM_EMAIL = "snchorsiya008@gmail.com"


LOGIN_REDIRECT_URL = 'blog:post_list'
LOGIN_URL = 'blog:login'
LOGOUT_URL = 'blog:logout'

# AUTH_PROFILE_MODULE = 'blog.base.Profile'


AUTHENTICATION_BACKENDS = [
 'django.contrib.auth.backends.ModelBackend',
 'blog.authentication.EmailAuthBackend',
]


AUTO_LOGOUT = {'SESSION_TIME': 10, 'message':'The Session has expired. Please login again to continue.',}
