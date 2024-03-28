"""
Django settings for sitewomen project.

Generated by 'django-admin startproject' using Django 4.2.1.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.2/ref/settings/
"""

from pathlib import Path
from django.conf.global_settings import AUTH_USER_MODEL, AUTHENTICATION_BACKENDS, DEFAULT_FROM_EMAIL, EMAIL_HOST_USER, EMAIL_USE_SSL, EMAIL_USE_TLS, LOGIN_REDIRECT_URL, LOGIN_URL, LOGOUT_REDIRECT_URL, SERVER_EMAIL
import environ


env = environ.Env()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

environ.Env.read_env(BASE_DIR / '.env')

################### VS CODE ###################
# В launch.json добавить параметр "cwd": "${workspaceFolder}/sitewomen",
# для установки рабочей директории по умолчанию

# env = environ.Env(
#     DEBUG=(bool, False),
#                   )


# env = environ.Env()
# env.read_env('.env')
# environment = env.str('ENV', default='dev')
# if environment == 'dev':
#     env_file = '.env-dev'
# elif environment == 'prod':
#     env_file = '.env-prod'
# else:
#     env_file = '.env-dev'
# env.read_env(env_file)

# пример синтаксиса .env

# ALLOWED_HOSTS=127.0.0.1,localhost,188.68.220.202
# ALLOWED_HOSTS = env.list('ALLOWED_HOSTS')

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-13j$s%lr!bp5z&vp+ef^m+bqfz!^=eh=z=s!b1af)!2#k0jh4#'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['127.0.0.1']

INTERNAL_IPS = ["127.0.0.1",]


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django_extensions',
    'women.apps.WomenConfig',
    "debug_toolbar",
    "users",
    'social_django',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    "debug_toolbar.middleware.DebugToolbarMiddleware",
]

ROOT_URLCONF = 'sitewomen.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            BASE_DIR / 'templates'    
        ],
        
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'users.context_processors.get_women_context',
            ],
        },
    },
]

WSGI_APPLICATION = 'sitewomen.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = 'ru-RU'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = 'static/'
STATICFILES_DIRS = [
    BASE_DIR / 'static'
]

# Рабочий вариант
# STATIC_URL = 'static/'
# if DEBUG:
#     STATICFILES_DIRS = (BASE_DIR / 'static',)
# else:
#     STATIC_ROOT = BASE_DIR / 'static'

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

LOGIN_REDIRECT_URL = 'home' # перенаправление после успешного входа в аккаунт
LOGOUT_REDIRECT_URL = 'home' # --
LOGIN_URL = 'users:login' # перенаправление после попытки зайти на закрытую страницу

# бекенды для авторизации пользователя
# можно написать дополнительные способы авторизация пользователя, наследовав BaseBackend
AUTHENTICATION_BACKENDS = [
    'social_core.backends.github.GithubOAuth2',
    'django.contrib.auth.backends.ModelBackend',
    'users.authentication.EmailAuthBackend',
]


DEFAULT_USER_IMAGE = MEDIA_URL + "users/default.png"

# если PostgreSQL
# SOCIAL_AUTH_JSONFIELD_ENABLED = True
# migrate

# по умолчанию auth.User, следует менять когда переопределяется модель для User
AUTH_USER_MODEL = 'users.User'

# EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend" # для теста писем в консоли

# if DEBUG:
#     EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

###
# EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend" 
EMAIL_BACKEND = 'sitewomen.backend.email.EmailBackend' # custom email Backend

##### yandex
# EMAIL_HOST_PASSWORD = "hnudeagzikenjpym" # пароль smtp yandex dj4ngo.t 

# EMAIL_HOST = "smtp.yandex.ru"
# EMAIL_PORT = 465 # 587
# EMAIL_HOST_USER = "dj4ngo.t@yandex.ru"
# EMAIL_USE_SSL = True
# EMAIL_USE_TLS = False

##### mail.ru
EMAIL_HOST_PASSWORD = "7aaf7KQBJmdymsnxLf9z"
EMAIL_HOST = "smtp.mail.ru"
EMAIL_PORT = 465
EMAIL_HOST_USER = "django.test@internet.ru"
EMAIL_USE_SSL = True
EMAIL_USE_TLS = False


DEFAULT_FROM_EMAIL = EMAIL_HOST_USER
SERVER_EMAIL = EMAIL_HOST_USER
EMAIL_ADMIN = EMAIL_HOST_USER


SOCIAL_AUTH_GITHUB_KEY = '19b318141366e9f6c6cd'
SOCIAL_AUTH_GITHUB_SECRET = '6f91cc9bc97a541a9d609fa372a5fc5894a05df2'

SOCIAL_AUTH_PIPELINE = (
    'social_core.pipeline.social_auth.social_details',
    'social_core.pipeline.social_auth.social_uid',
    'social_core.pipeline.social_auth.auth_allowed',
    'social_core.pipeline.social_auth.social_user',
    'social_core.pipeline.user.get_username',
    'social_core.pipeline.social_auth.associate_by_email',  # <--- enable this one
    'social_core.pipeline.user.create_user',
    # занесение пользователя в группу social при OAuth2
    'users.pipeline.new_users_handler',
    
    'social_core.pipeline.social_auth.associate_user',
    'social_core.pipeline.social_auth.load_extra_data',
    'social_core.pipeline.user.user_details',
)