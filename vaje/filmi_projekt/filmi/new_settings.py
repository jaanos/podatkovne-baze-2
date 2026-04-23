from settings import *
import environ
import os

env = environ.Env()
environ.Env.read_env(os.path.join(BASE_DIR, '.env'))

DATABASES = {
    'default' : {
        'ENGINE' : 'django.db.backends.postgresql',
        'NAME' : env('NAME'),
        'USER' : env('USER'),
        'PASSWORD' : env('PASSWORD'),
        'HOST' : env('HOST'),
        'PORT' : env('PORT'),
    }
}