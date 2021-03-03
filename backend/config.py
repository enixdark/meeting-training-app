import os
from dotenv import load_dotenv

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
load_dotenv(dotenv_path=os.path.join(BASE_DIR, ".env"), override=True)


class BaseApiConfig(object):
    DEBUG = False
    TESTING = False
    SECRET_KEY = '33423243434423RhSOm7GkRwHsJ1xERDH1mg='

    # flask google configuration.
    REDIRECT_URI = ''
    CLIENT_ID = ''
    CLIENT_SECRET = ''
    DATABASE_URI = 'mysql://127.0.0.1:3306'

    # flask celery configuration.
    CELERY_BROKER_URL = 'redis://localhost:6379/0
    CELERY_RESULT_BACKEND = 'redis://localhost:6379/0'
    CELERY_TASK_SERIALIZER = 'json'

    # Time config
    TIME_DIFFERENCE = 7
    CALENDAR_UPDATE_DELAY = 6
    EMAIL_UPDATE_DELAY = 6

    # Email config
    EMAIL_CONFIG = {
        'account': '',
        'username': '',
        'password': '',
        'smtp': '',
        'port': ''
    }


class WebApiConfig(BaseApiConfig):
    DEBUG = True


class MobileApiConfig(BaseApiConfig):
    DEBUG = True
