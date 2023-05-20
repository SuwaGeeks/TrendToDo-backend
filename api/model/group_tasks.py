from db import db, ma
from sqlalchemy.dialects.mysql import TIMESTAMP as Timestamp
from sqlalchemy.sql.functions import current_timestamp
from sqlalchemy import and_, or_

class GroupTasks(db.Model):
    __tablename__ = 'group_tasks'
    taskId = db.Column(db.Integer, autoincrement=True, primary_key=True)
    taskGroupId= db.Column(db.Integer, nullable=False)
    taskName = db.Column(db.String(225), nullable=False)
    taskContent= db.Column(db.String(225), nullable=False)
    taskLimit = db.Column(db.DateTime, nullable=False)
    taskWeight = db.Column(db.Integer, nullable=False)
    meanTime = db.Column(db.Integer, nullable=False)

    # Contructor
    def __init__(self, taskGroupId, taskName, taskContent, taskLimit, taskWeight=0, meanTime=0):
        self.taskGroupId = taskGroupId
        self.taskName = taskName
        self.taskContent = taskContent
        self.taskLimit = taskLimit
        self.taskWeight = taskWeight
        self.meanTime = meanTime

    def __repr__(self):
        return '<GroupTask %r>' % self.taskName
    
    # グループユーザの配列から、そのユーザが所属しているグループの全てのタスクを取得
    def get_group_tasks_by_group_user(group_users):
        groupIds = [and_(
            GroupTasks.taskGroupId == g['groupId'],
        ) for g in group_users]
        return db.session.query(GroupTasks) \
            .filter(or_(*groupIds)).all()

    #グループIDで指定したグループのタスク一覧を取得
    def get_group_tasks_by_group_id(group_id):
        return db.session.query(GroupTasks)\
            .filter(GroupTasks.taskGroupId == group_id)\
            .all()
    
    #指定したグループの指定したタスクの情報を取得
    def get_group_task_by_task_id(task_id):
        return db.session.query(GroupTasks)\
            .filter(GroupTasks.taskId == task_id)\
            .first()

    #グループIDで指定したグループに新しいタスクを追加
    def post_group_task_by_group_id(group_task):
        record=GroupTasks(
            taskGroupId=group_task['groupId'],
            taskName=group_task['taskName'],
            taskContent=group_task['taskContent'],
            taskLimit=group_task['taskLimit'],
        )
        db.session.add(record)
        db.session.commit()
        return record

    #指定したグループの指定したタスクの内容を変更
    def put_group_task_by_task_id(group_task, task_id):
        target_task=db.session.query(GroupTasks)\
            .filter(GroupTasks.taskId == task_id).first()
        target_task.taskName = group_task['taskName']
        target_task.taskContent = group_task['taskContent']
        target_task.taskLimit = group_task['taskLimit']
        db.session.commit()
        return target_task

    #指定したグループの指定したタスクを削除
    def delete_group_task(task_id):
        return db.session.query(GroupTasks)\
            .filter(GroupTasks.taskId == task_id).delete()


# Difinition of User Schema with Marshmallow
# refer: https://flask-marshmallow.readthedocs.io/en/latest/
class GroupTasksSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = GroupTasks