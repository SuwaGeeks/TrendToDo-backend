from flask import make_response, jsonify
from model.group_tasks import GroupTasks, GroupTasksSchema
from model.group_task_logs import GroupTaskLog, GroupTaskLogSchema
#ユーザIDで指定したユーザが所属しているグループのすべてのタスクを取得
def get_all_group_task_by_userId_logic(userId):
    return


#グループIDで指定したグループのタスク一覧を取得
def get_group_task_list_by_groupId_logic(groupId):
    groupTask_list=GroupTasks.get_group_tasks_by_group_id(groupId)
    groupTask_schema=GroupTasksSchema(many=True)#フォーマットを整えインスタンス化
    return make_response(jsonify({
        "code":200,
        "groupTasks":groupTask_schema.dump(groupTask_list)
    }))

#グループIDで指定したグループに新しいタスクを追加
def post_group_task_logic(req):
    groupTask=GroupTasks.post_group_task_by_group_id(req)
    groupTask_schema=GroupTasksSchema()#フォーマットを整えインスタンス化
    return make_response(jsonify({
        "code":200,
        "task":groupTask_schema.dump(groupTask)
    }))

#指定したグループの指定したタスクの情報を取得
def get_group_task_info_by_taskId_logic(taskId):
    groupTask=GroupTasks.get_group_task_by_task_id(taskId)
    groupTask_schema=GroupTasksSchema()
    return make_response(jsonify({
        "code":200,
        "task":groupTask_schema.dump(groupTask)
    }))

#指定したグループの指定したタスクの内容を変更
def put_group_task_info_logic(reqBody,taskId):
    groupTask=GroupTasks.put_group_task_by_task_id(reqBody,taskId)
    groupTask_schema=GroupTasksSchema()
    return make_response(jsonify({
        "code":200,
        "task":groupTask_schema.dump(groupTask)
    }))

#指定したグループの指定したタスクを削除
def delete_group_task_logic(taskId):
    GroupTasks.delete_group_task(taskId)
    return make_response(jsonify({"code":200}))

#グループタスクを消化する
def submit_group_task_logic(taskId):
    newlog=GroupTaskLog.add_group_task_log(taskId)
    groupTaskLog_schema=GroupTaskLogSchema()
    return make_response(jsonify({
        "code":200,
        "task":groupTaskLog_schema.dump(newlog)
    }))
