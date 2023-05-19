from db import db, ma
from sqlalchemy.dialects.mysql import TIMESTAMP as Timestamp
from sqlalchemy.sql.functions import current_timestamp

class Group(db.Model):
    __tablename__ = 'groups'
    groupId = db.Column(db.Integer, autoincrement=True, primary_key=True)
    groupName = db.Column(db.String(225), nullable=False)
    created_at = db.Column(Timestamp, server_default=current_timestamp(), nullable=False)
    updated_at = db.Column(Timestamp, server_default=current_timestamp(), nullable=False)

    # Contructor
    def __init__(self, groupId, groupName, created_at, updated_at):
        self.groupId = groupId
        self.groupName = groupName
        self.created_at = created_at
        self.updated_at = updated_at

    def __repr__(self):
         return '<Group %r>' % self.groupName

    def get_group_list():
        # SELECT * FROM users
        group_list = db.session.query(Group).all()
        if group_list == None:
            return []
        else:
            return group_list

    def get_user_by_id(id):
        return db.session.query(Group)\
            .filter(Group.groupId == id)\
            .one()

    def create_group(group):
        record = Group(
            groupName = group['name'],
        )
        # INSERT INTO group(groupName) VALUES(...)
        db.session.add(record)
        db.session.commit()
        return group

# Difinition of User Schema with Marshmallow
# refer: https://flask-marshmallow.readthedocs.io/en/latest/
class GroupSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
      model = Group