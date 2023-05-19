from db import db, ma
from sqlalchemy.dialects.mysql import TIMESTAMP as Timestamp
from sqlalchemy.sql.functions import current_timestamp

class GroupTaskLog(db.Model):
    __tablename__ = 'group_task_logs'
    refId = db.Column(db.Integer, autoincrement=True, primary_key=True)
    taskId = db.Column(db.Integer, nullable=False)
    taskGroupId = db.Column(db.Intege, nullable=False)
    finishedAt = db.Column(Timestamp, server_default=current_timestamp(), nullable=False)

    # Contructor
    def __init__(self, refId, taskId, taskGroupId, finishedAt):
        self.refId = refId
        self.taskId = taskId
        self.taskGroupId = taskGroupId
        self.finishedAt = finishedAt

    def __repr__(self):
        return '<GroupTaskLogs %r>' % self.taskId

    def get_group_task_log_list():
        # SELECT * FROM users
        group_task_log_list = db.session.query(GroupTaskLog).all()
        if group_task_log_list == None:
            return []
        else:
            return group_task_log_list
        
    def add_group_task_log(task_id, task_group_id):
        record = GroupTaskLog(
            taskId=task_id,
            taskGroupId=task_group_id,
        )
        db.session.add(record)
        db.session.commit()
        return task_id

    def get_group_task_log_by_task_id(task_id):
        return db.session.query(GroupTaskLog) \
            .filter(GroupTaskLog.taskId == task_id) \
            .one()

    def get_group_task_log_by_user_id(group_id):
        return db.session.query(GroupTaskLog) \
            .filter(GroupTaskLog.taskGroupId == group_id)

# Difinition of User Schema with Marshmallow
# refer: https://flask-marshmallow.readthedocs.io/en/latest/
class GroupTaskLogSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
      model = GroupTaskLog