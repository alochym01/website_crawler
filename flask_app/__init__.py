from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import sqlite3
app = Flask(__name__, instance_relative_config=True)

# load config settings for flask
app.config.from_object('config.settings')
app.config.from_pyfile('settings.py', silent=False)

db = SQLAlchemy(app)


from .blueprints.vtv import vtvs

# Blueprint Registration
app.register_blueprint(vtvs)
# from . import views
