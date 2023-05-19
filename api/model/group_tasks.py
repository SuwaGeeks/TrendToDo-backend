from db import db, ma
from sqlalchemy.dialects.mysql import TIMESTAMP as Timestamp
from sqlalchemy.sql.functions import current_timestamp

class GroupTasks(db.Model):
    __tablename__ = 'group_tasks'
    taskId = db.Column(db.Integer, autoincrement=True, primary_key=True)
    taskGroupId= db.Column(db.Integer, nullable=False)
    taskName = db.Column(db.String(225), nullable=False)
    taskContent= db.Column(db.String(225), nullable=False)
    taskLimit = db.Column(db.Datatime, nullable=False)
    taskWeight = db.Column(db.Integer, nullable=False)
    meanTime = db.Column(db.Integer, nullable=False)

    # Contructor
    def __init__(self, taskId, taskGroupId, taskName, taskContent, taskLimit, taskWeight, meanTime):
        self.taskId = taskId
        self.taskGroupId = taskGroupId
        self.taskName = taskName
        self.taskContent = taskContent
        self.taskLimit = taskLimit
        self.taskWeight = taskWeight
        self.meanTime = meanTime

    def __repr__(self):
        return '<GroupTask %r>' % self.taskName
    
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
    def add_group_task_by_group_id(group_task):
        record=GroupTasks(
            taskGroupId=group_task["taskGroupId"],
            taskName=group_task['taskName'],
            taskContent=group_task['taskContent'],
            taskLimit=group_task['taskLimit'],
        )
        db.session.add(record)
        db.session.commit()
        return group_task

    #指定したグループの指定したタスクの内容を変更
    def change_group_task(group_task):
        target_task = db.session.query(GroupTasks)\
            .filter(GroupTasks.taskId == group_task["taskId"]).first()
        target_task.taskName = group_task['taskName']
        target_task.taskContent = group_task['taskContent']
        target_task.taskLimit = group_task['taskLimit']
        db.session.commit()
        return group_task

    #指定したグループの指定したタスクを削除
    def delete_group_task(task_id):
        return db.session.query(GroupTasks)\
            .filter(GroupTasks.taskId == task_id).delete()


        
# Difinition of User Schema with Marshmallow
# refer: https://flask-marshmallow.readthedocs.io/en/latest/
class GroupTasksSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
      model = GroupTasks