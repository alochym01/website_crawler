import os

BASEDIR = os.path.abspath(os.path.dirname(__file__))
TOP_LEVEL_DIR = os.path.abspath(os.curdir)

SECRET_KEY = '\xc0\x1fPr;%2H\xcd1$/\xa9\xcb\nZ\x89\x8e^2\xde\xbb\xfcC'
DEBUG = True

WTF_CSRF_ENABLED = True

BCRYPT_LOG_ROUNDS = 10

DEBUG_TB_INTERCEPT_REDIRECTS = False

SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(BASEDIR, 'app.db')
SQLALCHEMY_TRACK_MODIFICATIONS = False


PER_PAGE = 10
CSS_FRAMEWORK = 'bootstrap4'
SHOW_SINGLE_PAGE = False
ALIGNMENT = 'center'
LINK_SIZE = 'sm'

CELERY_BROKER_URL = 'redis://localhost:6379/0'
CELERY_RESULT_BACKEND = 'redis://localhost:6379/1'
CELERYD_LOG_FILE = os.path.join(BASEDIR, 'celery.log')
