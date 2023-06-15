from db import db, ma
from sqlalchemy.dialects.mysql import TIMESTAMP as Timestamp
from sqlalchemy.sql.functions import current_timestamp
from sqlalchemy import and_, or_

class Group(db.Model):
    __tablename__ = 'groups'
    groupId = db.Column(db.Integer, autoincrement=True, primary_key=True)
    groupName = db.Column(db.String(225), nullable=False)
    created_at = db.Column(Timestamp, server_default=current_timestamp(), nullable=False)
    updated_at = db.Column(Timestamp, server_default=current_timestamp(), nullable=False)

    # Contructor
    def __init__(self, groupName):
        self.groupName = groupName

    def __repr__(self):
         return '<Group %r>' % self.groupName

    def get_group_list():
        # SELECT * FROM users
        group_list = db.session.query(Group).all()
        if group_list == None:
            return []
        else:
            return group_list

    def get_user_by_groupId(groupId):
        return db.session.query(Group)\
            .filter(Group.groupId == groupId)\
            .one()
    
    # グループIDで指定したグループの情報を取得する
    def get_group_info_by_groupId(groupId):
        return db.session.query(Group) \
            .filter(Group.groupId == groupId) \
            .one()
    
    # グループ名からグループを取得する
    def get_group_by_groupName(groupName):
        return db.session.query(Group) \
            .filter(Group.groupName == groupName).all()

    def create_group(group):
        record = Group(
            groupName = group['groupName'],
        )
        # INSERT INTO group(groupName) VALUES(...)
        db.session.add(record)
        db.session.commit()
        return record
    
    # グループユーザの情報から全てのグループを取得する
    def get_groupList_from_group_user(group_users):
        groupIds = [and_(
            Group.groupId == g['groupId'],
        ) for g in group_users]
        return db.session.query(Group) \
            .filter(or_(*groupIds)).all()

# Difinition of User Schema with Marshmallow
# refer: https://flask-marshmallow.readthedocs.io/en/latest/
class GroupSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
      model = Group