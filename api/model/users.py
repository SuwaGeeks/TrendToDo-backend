from db import db, ma
from sqlalchemy.dialects.mysql import TIMESTAMP as Timestamp
from sqlalchemy.sql.functions import current_timestamp

class User(db.Model):
    __tablename__ = 'users'
    userId = db.Column(db.Integer, autoincrement=True, primary_key=True)
    userName = db.Column(db.String(225), nullable=False)
    password = db.Column(db.String(300), nullable=False)
    created_at = db.Column(Timestamp, server_default=current_timestamp(), nullable=False)
    updated_at = db.Column(Timestamp, server_default=current_timestamp(), nullable=False)

    # Contructor
    def __init__(self, userId, userName, password, created_at, updated_at):
        self.userId = userId
        self.userName = userName
        self.password = password
        self.created_at = created_at
        self.updated_at = updated_at

    def __repr__(self):
         return '<User %r>' % self.userName

    # ユーザリストを取得する
    def get_user_list():
        # SELECT * FROM users
        user_list = db.session.query(User).all()
        if user_list == None:
            return []
        else:
            return user_list

    # ユーザの情報を変更する
    def change_user(user):
        tagetUser = db.session.query(User) \
            .filter(User.userId == user["userId"]).one()
        tagetUser.userName = user["taskName"],
        tagetUser.password = user["taskContent"],
        db.session.commit()
        return user

    # 新しいユーザを追加する
    def create_user(user):
        record = User(
            name = user['name'],
        )
        # INSERT INTO users(name) VALUES(...)
        db.session.add(record)
        db.session.commit()
        return user
    
    def get_user_by_id(id):
        return db.session.query(User)\
            .filter(User.id == id)\
            .one()

# Difinition of User Schema with Marshmallow
# refer: https://flask-marshmallow.readthedocs.io/en/latest/
class UserSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
      model = User