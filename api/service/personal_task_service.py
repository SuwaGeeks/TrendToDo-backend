from flask import make_response, jsonify
import datetime
from model.personal_tasks import PersonalTask, PersonalTaskSchema
from model.personal_task_logs import PersonalTaskLog, PersonalTaskLogSchema


#個人タスクの一覧を取得
def get_personal_task_logic(userId):
    personal_task_schema_list = PersonalTaskSchema(many=True)
    personal_task_log_schema = PersonalTaskLogSchema(many=True)

    tasks = PersonalTask.get_personal_task_by_user_id(userId)
    tasks = personal_task_schema_list.dump(tasks)

    logs = PersonalTaskLog.get_personal_task_log_by_user_id(userId)
    logs = personal_task_log_schema.dump(logs)

    id2index = {}
    for i in range(len(tasks)):
        tasks[i]['finished_at'] = ''
        id2index[tasks[i]['taskId']] = i

    for log in logs:
        tasks[id2index[log['taskId']]]['finished_at'] = log['finishedAt']

    return make_response(jsonify({
        'code': 200,
        'userTasks': tasks
    }))
    
#新しい個人タスクを追加
def add_new_personal_task_logic(req, userId):
    personal_task_schema = PersonalTaskSchema()
    req['taskLimit'] = datetime.date.fromisoformat(req['taskLimit'])
    req['userId'] = userId
    task = PersonalTask.add_personal_task(req)
    return make_response(jsonify({
        'code': 200,
        'task': personal_task_schema.dump(task)
    }))

#タスクIDで指定したタスクの情報を取得
def get_personal_task_by_taskId_logic(taskId):
    personal_task_schema = PersonalTaskSchema()
    task = PersonalTask.get_personal_task_by_task_id(taskId)
    return make_response(jsonify({
        'code': 200,
        'task': personal_task_schema.dump(task)
    }))

#タスクIDで指定したタスクの内容を変更
def change_personal_task_logic(req, taskId):
    personal_task_schema = PersonalTaskSchema()
    req['taskId'] = taskId
    task = PersonalTask.change_personal_task(req)
    return make_response(jsonify({
        'code': 200,
        'task': personal_task_schema.dump(task)
    }))

#タスクIDで指定したタスクを削除
def delete_personal_task_logic(taskId):
    PersonalTask.delete_personal_task(taskId)
    return make_response(jsonify({'code': 200}))

#個人タスクを消化する
def submit_personal_task_logic(taskId):
    targetTask = PersonalTask.get_personal_task_by_task_id(taskId)

    newLog = PersonalTaskLog.add_personal_task_log(taskId, targetTask['hostUserId'])
    personal_task_log_schema = PersonalTaskLogSchema()
    return make_response(jsonify({
        'code': 200,
        'log': personal_task_log_schema.dump(newLog),
    }))