from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import sqlite3
# from celery import Celery
from .celery_init import make_celery

app = Flask(__name__, instance_relative_config=True)

# load config settings for flask
app.config.from_object('config.settings')
app.config.from_pyfile('settings.py', silent=False)

# load Celery config
celery_app = make_celery(app)

# initial db
db = SQLAlchemy(app)

# import blueprints after initial db
from .blueprints.vtv import vtvs
from .blueprints.youtube import youtube

# Blueprint Registration
app.register_blueprint(vtvs)
app.register_blueprint(youtube)
# from . import views
