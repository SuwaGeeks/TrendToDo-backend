from db import db, ma
from sqlalchemy.dialects.mysql import TIMESTAMP as Timestamp
from sqlalchemy.sql.functions import current_timestamp

# 個人タスク
class PersonalTask(db.Model):
    __tablename__ = 'personal_tasks'
    taskId = db.Column(db.Integer, autoincrement=True, primary_key=True)
    hostUserId = db.Column(db.Integer, nullable=False)
    taskName = db.Column(db.String(225), nullable=False)
    taskContent = db.Column(db.String(225), nullable=False)
    taskLimit = db.Column(db.DateTime, nullable=False)
    created_at = db.Column(Timestamp, server_default=current_timestamp(), nullable=False)
    updated_at = db.Column(Timestamp, server_default=current_timestamp(), nullable=False)

    # Contructor
    def __init__(self, hostUserId, taskName, taskContent, taskLimit):
        self.hostUserId = hostUserId
        self.taskName = taskName
        self.taskContent = taskContent
        self.taskLimit = taskLimit

    def __repr__(self):
        return '<PersonalTasks %r>' % self.taskName

    #個人タスクの一覧を取得
    def get_personal_task_list():
        # SELECT * FROM users
        persnal_task_list = db.session.query(PersonalTask).all()
        if persnal_task_list == None:
            return []
        else:
            return persnal_task_list

    #タスクIDで指定したタスクの情報を取得
    def get_personal_task_by_task_id(task_id):
        return db.session.query(PersonalTask) \
            .filter(PersonalTask.taskId == task_id) \
            .one()

    #ユーザIDで指定したタスクの情報を取得
    def get_personal_task_by_user_id(user_id):
        return db.session.query(PersonalTask) \
            .filter(PersonalTask.hostUserId == user_id).all()

    #新しい個人タスクの追加
    def add_personal_task(personal_task):
        record = PersonalTask(
            hostUserId=personal_task["userId"],
            taskName = personal_task["taskName"],
            taskContent = personal_task["taskContent"],
            taskLimit = personal_task["taskLimit"],
        )
        db.session.add(record)
        db.session.commit()
        return personal_task

    #タスクIDで指定したタスクの情報を変更
    def change_personal_task(personal_task):
        targetTaks = db.session.query(PersonalTask) \
            .filter(PersonalTask.taskId == personal_task["taskId"]).one()
        targetTaks.taskName = personal_task["taskName"],
        targetTaks.taskContent = personal_task["taskContent"],
        targetTaks.taskLimit = personal_task["taskLimit"],
        db.session.commit()
        return targetTaks

    #タスクIDで指定したタスクを削除
    def delete_personal_task(task_id):
        return db.session.query(PersonalTask) \
            .filter(PersonalTask.taskId == task_id).delete()

# Difinition of User Schema with Marshmallow
# refer: https://flask-marshmallow.readthedocs.io/en/latest/
class PersonalTaskSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
      model = PersonalTask