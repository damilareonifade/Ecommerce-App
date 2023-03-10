
from pathlib import Path
from dotenv import load_dotenv
load_dotenv() 
import os
BASE_DIR = Path(__file__).resolve().parent.parent


# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = str(os.getenv('SECRET_KEY'))

DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.postgres',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'commerce',
    'accounts',
    'crispy_forms',
    'cloudinary',
    'cloudinary_storage',
    'mptt',
    'cart',
    'seller',
    'django_social_share',
    'checkout',
    'notification',
    'orders',
    'oauth2_provider',
    "django.contrib.sites",
    "allauth",
    "allauth.account",
    "allauth.socialaccount",
    "allauth.socialaccount.providers.google",
    
 ]



MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    # 'accounts.middleware.DashboardMiddleware',
]

ROOT_URLCONF = 'ecommerce.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR,'templates/'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'commerce.context_processor.category_list',
                'commerce.context_processor.saved_post_count',
                'cart.context_processor.basket',
                'notification.context_processor.notification_list',
            ],
        },
    },
]

WSGI_APPLICATION = 'ecommerce.wsgi.application'
SITE_ID = 1


# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        "NAME": "postgres",
        'USER': "postgres",
        "PASSWORD": "postgres",
        'HOST': '',
        'PORT': "5432",
    }
}


# Password validation
# https://docs.djangoproject.com/en/4.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/4.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


LANGUAGES = [
    ('ar', ('Arabic')),
    ('en', ('English')),
]


STATIC_URL = 'static/'
STATIC_ROOT = os.path.join(BASE_DIR,'staticfiles')
STATICFILES_DIRS = (os.path.join(BASE_DIR,'static'),)

MEDIA_URL = 'media/'
DEFAULT_FILE_STORAGE = 'cloudinary_storage.storage.MediaCloudinaryStorage'
# MEDIA_ROOT = BASE_DIR/'media'

#default user model
AUTH_USER_MODEL = 'accounts.CustomUser'
LOGIN_URL = '/accounts/login'
LOGOUT_URL = '/accounts/logout'

#email_backend
EMAIL_BACKEND ='django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = "smtp.gmail.com"
EMAIL_HOST_USER = str(os.getenv('EMAIL_HOST_USER'))
EMAIL_HOST_PASSWORD = str(os.getenv('EMAIL_HOST_PASSWORD'))
EMAIL_PORT = 587
EMAIL_USE_TLS = True

FLUTTERWAVE_PUBLIC_KEY = str(os.getenv('FLUTTERWAVE_PUBLIC_KEY'))
FLUTTERWAVE_SECRET_KEY = str(os.getenv("FLUTTERWAVE_SECRET_KEY"))
FLUTTERWAVE_ENCRYPTION_KEY = str(os.getenv("FLUTTERWAVE_ENCRYPTION_KEY"))

SESSION_EXPIRE_AT_BROWSER_CLOSE = True
SESSION_AGE = 2400

CLOUDINARY_STORAGE = {
    'CLOUD_NAME': str(os.getenv("CLOUD_NAME")),
    'API_KEY': str(os.getenv("API_KEY")),
    'API_SECRET': str(os.getenv("API_SECRET"))
}

CRISPY_TEMPLATE_PACK = 'bootstrap4'
CART_ID = 'cart'
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

ACCOUNT_USER_MODEL_USERNAME_FIELD = 'email'
ACCOUNT_UNIQUE_EMAIL = True
# ACCOUNT_USERNAME_REQUIRED = False

AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
    #phone number login
    "accounts.user_model_backend.PhoneNumberBackend",
    'allauth.account.auth_backends.AuthenticationBackend',
    # 'allauth.socialaccount.providers.google.auth.GoogleOAuth2Adapter',
    # 'allauth.socialaccount.providers.google.provider.GoogleProvider',
]