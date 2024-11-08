import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

STATIC_URL = '/static/'
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'app', 'resources', 'static'),
]

SECRET_KEY = 'django-insecure-(w(l$&o#*bwi=7sd1^+4q&1%%t#je+cov9)2)l4jg7v1$$+&&1'
DEBUG = True
ALLOWED_HOSTS = [
    '*'
]
LOGIN_REDIRECT_URL = '/'
AUTH_USER_MODEL = 'app.CustomUser' # auth_user 를 커스텀함



''' Facebook API 사용
'''
BASE_REDIRECT_URI = 'https://274c-210-110-128-79.ngrok-free.app'
FACEBOOK_APP_ID = '1132533228242987'
FACEBOOK_APP_SECRET = '7d2284caffcb3722744e3b1f972f7d16'
FACEBOOK_REDIRECT_URI = f"{BASE_REDIRECT_URI}/facebook/callback/"

''' Instagram API 사용
'''
INSTAGRAM_APP_ID = '840583054818757'
INSTAGRAM_APP_SECRET = '6b5c79469e46456ac9ed742141e2f39c'
INSTAGRAM_REDIRECT_URI = f"{BASE_REDIRECT_URI}/instagram/callback/"

''' Kakao API 사용
'''
KAKAO_REST_API_KEY = '3e593285350a48ef8153776257682e76'

''' Naver API 사용
'''
NAVER_CLIENT_ID = 'f_kYLczHBJBSV3ElFbci'
NAVER_CLIENT_SECRET = 'ovYtXAG3vf'




INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'app',
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

ROOT_URLCONF = 'myproject.urls'

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

WSGI_APPLICATION = 'myproject.wsgi.application'

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
USE_L10N = True
USE_TZ = True
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
