from db import db, ma
from sqlalchemy.dialects.mysql import TIMESTAMP as Timestamp
from sqlalchemy.sql.functions import current_timestamp
from sqlalchemy.sql import func

class GroupTaskLog(db.Model):
    __tablename__ = 'group_task_logs'
    refId = db.Column(db.Integer, autoincrement=True, primary_key=True)
    taskId = db.Column(db.Integer, nullable=False)
    userId = db.Column(db.Integer, nullable=False)
    taskGroupId = db.Column(db.Integer, nullable=False)
    taskWeight = db.Column(db.Integer)
    taskTime = db.Column(db.Integer, nullable=False)
    finishedAt = db.Column(Timestamp, server_default=current_timestamp(), nullable=False)

    # Contructor
    def __init__(self, taskId, userId, taskGroupId, taskWeight, taskTime):
        self.taskId = taskId
        self.userId = userId
        self.taskGroupId = taskGroupId
        self.taskWeight = taskWeight
        self.taskTime = taskTime

    def __repr__(self):
        return '<GroupTaskLogs %r>' % self.taskId

    def get_group_task_log_list():
        # SELECT * FROM users
        group_task_log_list = db.session.query(GroupTaskLog).all()
        if group_task_log_list == None:
            return []
        else:
            return group_task_log_list
        
    # グループタスクを消化したときのログを追加
    def add_group_task_log(req):
        record = GroupTaskLog(
            taskId=req['taskId'],
            taskGroupId=req['groupId'],
            taskWeight=req['taskWeght'],
            taskTime=req['taskTime'],
            userId=req['userId']
        )
        db.session.add(record)
        db.session.commit()
        return record

    def get_group_task_log_by_task_id(task_id):
        return db.session.query(GroupTaskLog) \
            .filter(GroupTaskLog.taskId == task_id) \
            .one()

    def get_group_task_log_by_user_id(group_id):
        return db.session.query(GroupTaskLog) \
            .filter(GroupTaskLog.taskGroupId == group_id)
    
    # タスクIDからそのタスクの評価を計算する
    def calc_group_task_weight_by_task_id(task_id):
        return db.session.query(func.avg(GroupTaskLog.taskWeight).label("weight")) \
            .filter(GroupTaskLog.taskId == task_id).all()
    
    # タスクIDからそのタスクの平均時間を計算する
    def calc_group_task_time_by_task_id(task_id):
        return db.session.query(func.avg(GroupTaskLog.taskTime).label("taskTime")) \
            .filter(GroupTaskLog.taskId == task_id).all()

# Difinition of User Schema with Marshmallow
# refer: https://flask-marshmallow.readthedocs.io/en/latest/
class GroupTaskLogSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
      model = GroupTaskLog