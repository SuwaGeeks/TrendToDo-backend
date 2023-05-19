from main import app
from db import db

with app.app_context():
    db.drop_all()