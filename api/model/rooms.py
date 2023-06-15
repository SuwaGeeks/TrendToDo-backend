from db import db, ma
from sqlalchemy.dialects.mysql import TIMESTAMP as Timestamp
from sqlalchemy.sql.functions import current_timestamp

class Room(db.Model):
    __tablename__ = 'rooms'
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    name = db.Column(db.String(225), nullable=False)
    created_at = db.Column(Timestamp, server_default=current_timestamp(), nullable=False)
    updated_at = db.Column(Timestamp, server_default=current_timestamp(), nullable=False)

    # Contructor
    def __init__(self, id, name, created_at, updated_at):
        self.id = id
        self.name = name
        self.created_at = created_at
        self.updated_at = updated_at

    def __repr__(self):
         return '<User %r>' % self.name

    def get_user_list():
        # SELECT * FROM users
        user_list = db.session.query(User).all()
        if user_list == None:
            return []
        else:
            return user_list

    def get_user_by_id(id):
        return db.session.query(User)\
            .filter(User.id == id)\
            .one()

    def create_user(user):
        record = User(
            name = user['name'],
        )
        # INSERT INTO users(name) VALUES(...)
        db.session.add(record)
        db.session.commit()
        return user

# Difinition of User Schema with Marshmallow
# refer: https://flask-marshmallow.readthedocs.io/en/latest/
class UserSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
      model = User