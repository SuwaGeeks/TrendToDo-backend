from db import db, ma
from sqlalchemy.dialects.mysql import TIMESTAMP as Timestamp
from sqlalchemy.sql.functions import current_timestamp

# 個人タスク
class GroupUser(db.Model):
    __tablename__ = 'group_users'
    refId = db.Column(db.Integer, autoincrement=True, primary_key=True)
    userId =  db.Column(db.Integer, nullable=False)
    groupId =  db.Column(db.Integer, nullable=False)
    created_at = db.Column(Timestamp, server_default=current_timestamp(), nullable=False)

    # Contructor
    def __init__(self, refId, userId, groupId, created_at):
        self.refId = refId
        self.userId = userId
        self.groupId = groupId
        self.created_at = created_at

    def __repr__(self):
        return '<GroupUser %r>' % self.refId
    
    # ユーザIDで指定したユーザが所属しているグループを全て取得
    def get_all_group_by_user_id(user_id):
        return db.session.query(GroupUser)\
            .filter(GroupUser.userId == user_id).all()
    
    # グループIDで指定したグループに所属しているユーザをすべて取得
    def get_all_user_by_group_id(group_id):
        return db.session.query(GroupUser) \
            .filter(GroupUser.groupId == group_id).all()

    # ユーザが新しいグループに参加する
    def user_join_group(user_join):
        record = GroupUser(
            userId=user_join["userId"],
            groupId=user_join["groupId"]
        )
        db.session.add(record)
        db.session.commit()
        return user_join

    # ユーザがグループから退出する
    def user_exit_group(user_exit):
        return db.session.query(GroupUser) \
            .filter(GroupUser.groupId == user_exit["groupId"] and GroupUser.userId == user_exit["userId"]).delete()

# Difinition of User Schema with Marshmallow
# refer: https://flask-marshmallow.readthedocs.io/en/latest/
class GroupUserSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
      model = GroupUser

