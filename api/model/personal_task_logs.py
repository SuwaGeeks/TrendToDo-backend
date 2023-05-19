from db import db, ma
from sqlalchemy.dialects.mysql import TIMESTAMP as Timestamp
from sqlalchemy.sql.functions import current_timestamp

# 個人タスクのログ
class PersonalTaskLog(db.Model):
    __tablename__ = 'personal_task_logs'
    refId = db.Column(db.Integer, autoincrement=True, primary_key=True)
    taskId = db.Column(db.Integer, nullable=False)
    hostUserId = db.Column(db.Intege, nullable=False)
    finishedAt = db.Column(Timestamp, server_default=current_timestamp(), nullable=False)

    # Contructor
    def __init__(self, refId, taskId, hostUserId, finishedAt):
        self.refId = refId
        self.taskId = taskId
        self.hostUserId = hostUserId
        self.finishedAt = finishedAt

    def __repr__(self):
        return '<PersonalTaskLogs %r>' % self.taskId

    # 個人タスクのログを全て取得する
    def get_personal_task_log_list():
        # SELECT * FROM users
        personal_task_log_list = db.session.query(PersonalTaskLog).all()
        if personal_task_log_list == None:
            return []
        else:
            return personal_task_log_list
        
    # 個人タスクのログを新たに追加する
    def add_personal_task_log(personal_task):
        record = PersonalTaskLog(
            taskId=personal_task["taskId"],
            hostUserId=personal_task["userId"],
        )
        db.session.add(record)
        db.session.commit()
        return personal_task

    # 個人タスクのログを、タスクのIDで取得する
    def get_personal_task_log_by_task_id(task_id):
        return db.session.query(PersonalTaskLog) \
            .filter(PersonalTaskLog.taskId == task_id) \
            .one()

    # 個人タスクのログをユーザIDで全て取得する
    def get_personal_task_log_by_user_id(user_id):
        return db.session.query(PersonalTaskLog) \
            .filter(PersonalTaskLog.hostUserId == user_id)

# Difinition of User Schema with Marshmallow
# refer: https://flask-marshmallow.readthedocs.io/en/latest/
class PersonalTaskLogSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
      model = PersonalTaskLog