from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
SECRET_KEY = 'django-insecure-(w(l$&o#*bwi=7sd1^+4q&1%%t#je+cov9)2)l4jg7v1$$+&&1'
DEBUG = True
ALLOWED_HOSTS = [
    '*'
]
LOGIN_REDIRECT_URL = '/'

AUTH_USER_MODEL = 'app.CustomUser'      # auth_user 를 커스텀함

REDIRECT_URI = 'https://c2e0-210-110-128-122.ngrok-free.app'

''' Facebook OAuth API 사용
- Facebook Developer에서 제공된 App ID로 교체
- Facebook Developer에서 제공된 App Secret으로 교체
- 페이스북 인증 후 리디렉션될 URL 설정
'''
FACEBOOK_APP_ID = '499957726380843'
FACEBOOK_APP_SECRET = 'd0b71af16662111d1e6339272f59fd61'
FACEBOOK_REDIRECT_URI = 'https://c2e0-210-110-128-122.ngrok-free.app/facebook/callback/'

''' Naver API 사용
'''
NAVER_CLIENT_ID = 'y5WpwyV7pAd4iQygcMQl'
NAVER_CLIENT_SECRET = 'UNW6uToksE'
NAVER_REDIRECT_URI = f'{REDIRECT_URI}/naver/callback/'

''' KAKAO API 사용
'''
KAKAO_CLIENT_ID = ''

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
STATIC_URL = '/static/'
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
