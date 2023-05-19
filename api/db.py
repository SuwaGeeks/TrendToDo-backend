from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

db = SQLAlchemy()
ma = Marshmallow()

def init_db(app):
  db.init_app(app)

def init_ma(app):
  ma.init_app(app)