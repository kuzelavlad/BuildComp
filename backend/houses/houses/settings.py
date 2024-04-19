from pathlib import Path
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect

import os

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = 'django-insecure-t)@q0-6z&($ki529b==7xk936k()ucqt+3+v!gkpp0@jy3yn)2'

DEBUG = True

ALLOWED_HOSTS = ['aroma-stroy-by', 'www.aroma-stroy.by', '178.172.201.190', '127.0.0.1']

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',



    'housestroy.apps.HousestroyConfig',
    'contacts.apps.ContactsConfig',
    'blog.apps.BlogConfig',
    'personal.apps.PersonalConfig',
    'application.apps.ApplicationConfig',
    'revenge.apps.RevengeConfig',

    'rest_framework',
    'django_filters',
    'corsheaders',
    'ckeditor',

]

REST_FRAMEWORK = {
    'DEFAULT_FILTER_BACKENDS': ['django_filters.rest_framework.DjangoFilterBackend'],
    'DEFAULT_PARSER_CLASSES': (
        'rest_framework.parsers.JSONParser',
        'rest_framework.parsers.FormParser',
        'rest_framework.parsers.MultiPartParser',
    ),
}

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
]

ROOT_URLCONF = 'houses.urls'

# CORS_ALLOWED_ORIGINS = ['https://aroma-stroy.by', 'http://192.168.0.104:8000']

CORS_ALLOW_ALL_ORIGINS = True
CORS_ALLOW_METHODS = (
    "GET",
    "PATCH",
    "POST",
)

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

WSGI_APPLICATION = 'houses.wsgi.application'

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": "HouseStroyDB",
        # "NAME": "/var/www/database/HouseStroyDB", так надо на проде
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


LANGUAGE_CODE = 'ru'

TIME_ZONE = 'Europe/Minsk'

USE_I18N = True

USE_TZ = True


STATIC_URL = 'static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')


EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.yandex.ru'
EMAIL_PORT = 465
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'Alfa-Building@yandex.by'
EMAIL_HOST_PASSWORD = 'znlbywpfoealoqjo'
DEFAULT_FROM_EMAIL = 'Alfa-Building@yandex.by'


CKEDITOR_UPLOAD_PATH = "uploads/"
CKEDITOR_JQUERY_URL = 'https://ajax.googleapis.com/ajax/libs/jquery/3.6.0/jquery.min.js'  # URL для jQuery
CKEDITOR_CONFIGS = {
    'default': {
        'toolbar': 'full',
        'height': 300,
        'width': 600,
    },
}


AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',  # Аутентификация на основе модели User
)

LOGIN_URL = '/admin/'


def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('admin')  # Перенаправление на домашнюю страницу после успешной аутентификации
        else:
            # Обработка ошибки аутентификации
            return render(request, 'admin', {'error_message': 'Неправильное имя пользователя или пароль.'})
    # else:
    #     return render(request, 'login.html')
