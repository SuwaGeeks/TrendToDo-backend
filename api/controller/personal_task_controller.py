from service.personal_task_service import *

#個人タスクの一覧を取得
def get_personal_task_list(userId):
    return get_personal_task_logic(userId)
    
#新しい個人タスクを追加
def post_personal_task(reqBody, userId):
    return add_new_personal_task_logic(reqBody, userId)

#タスクIDで指定したタスクの情報を取得
def get_personal_task_by_taskId(userId, taskId):
    return get_personal_task_by_taskId_logic(userId, taskId)

#タスクIDで指定したタスクの内容を変更
def put_personal_task_by_taskId(reqBody, taskId):
    return change_personal_task_logic(reqBody, taskId)

#タスクIDで指定したタスクを削除
def delete_personal_task_by_taskId(taskId):
    return delete_personal_task_logic(taskId)

#個人タスクを消化する
def submit_personal_task(taskId):
    return submit_personal_task_logic(taskId)