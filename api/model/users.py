from db import db, ma
from sqlalchemy.dialects.mysql import TIMESTAMP as Timestamp
from sqlalchemy.sql.functions import current_timestamp
from sqlalchemy import and_, or_

class User(db.Model):
    __tablename__ = 'users'
    userId = db.Column(db.Integer, autoincrement=True, primary_key=True)
    userName = db.Column(db.String(225), nullable=False)
    password = db.Column(db.String(300), nullable=False)
    created_at = db.Column(Timestamp, server_default=current_timestamp(), nullable=False)
    updated_at = db.Column(Timestamp, server_default=current_timestamp(), nullable=False)

    # Contructor
    def __init__(self, userName, password):
        self.userName = userName
        self.password = password

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

    # ユーザ名を変更する
    def change_user_name(userName, userId):
        targetUser = db.session.query(User) \
            .filter(User.userId == userId).one()
        targetUser.userName = userName
        db.session.commit()
        return targetUser
    
    # パスワードを変更する
    def change_user_password(password, userId):
        targetUser = db.session.query(User) \
            .filter(User.userId == userId).one()
        targetUser.password = password
        db.session.commit()
        return targetUser

    # 新しいユーザを追加する
    def create_user(user):
        record = User(
            userName = user['userName'],
            password = user['password'],
        )
        # INSERT INTO users(name) VALUES(...)
        db.session.add(record)
        db.session.commit()
        return record
    
    def get_user_by_id(id):
        return db.session.query(User)\
            .filter(User.id == id)\
            .one()
    
    # パスワードとユーザ名とIDでユーザ認証をする
    def check_user(user):
        return db.session.query(User) \
            .filter(User.userName == user['userName']) \
            .filter(User.password == user['password']).all()
    
    # グループユーザの配列からユーザ情報を取得する
    def get_user_list_from_group_user(group_users):
        groupIds = [and_(
            User.userId == g['userId'],
        ) for g in group_users]
        return db.session.query(User) \
            .filter(or_(*groupIds)).all()

# Difinition of User Schema with Marshmallow
# refer: https://flask-marshmallow.readthedocs.io/en/latest/
class UserSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
      model = User