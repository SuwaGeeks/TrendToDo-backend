from service.group_task_service import *

#ユーザIDで指定したユーザが所属しているグループのすべてのタスクを取得
def get_all_group_task_by_userId(userId):
    return get_all_group_task_by_userId_logic(userId)

#グループIDで指定したグループのタスク一覧を取得
def get_group_task_list_by_groupId(groupId):
    return get_group_task_list_by_groupId_logic(groupId)

#グループIDで指定したグループに新しいタスクを追加
def post_group_task(reqBody):
    return post_group_task_logic(reqBody)

#指定したグループの指定したタスクの情報を取得
def get_group_task_info_by_taskId(taskId):
    return get_group_task_info_by_taskId_logic(taskId)

#指定したグループの指定したタスクの内容を変更
def put_group_task_info(reqBody,taskId):
    return put_group_task_info_logic(reqBody,taskId)

#指定したグループの指定したタスクを削除
def delete_group_task(taskId):
    return delete_group_task_logic(taskId)

#グループタスクを消化する
def submit_group_task(taskId):
    return submit_group_task_logic(taskId)