from flask import make_response, jsonify
from model.groups import Group, GroupSchema
from model.group_users import GroupUser, GroupUserSchema
from model.group_tasks import GroupTasks, GroupTasksSchema
from model.group_task_logs import GroupTaskLog, GroupTaskLogSchema
from model.users import User, UserSchema

#ユーザIDで指定したユーザが所属しているグループのすべてのタスクを取得
def get_all_group_task_by_userId_logic(userId):
    return

# グループのレスポンスモデルを作成する関数
def create_group_response_model(group):
    group_schema = GroupSchema()
    group = group_schema.dump(group)
    groupId = group["groupId"]

    group_user_schema = GroupUserSchema(many=True)
    groupUsers = GroupUser.get_all_user_by_group_id(groupId)
    groupUsers = group_user_schema.dump(groupUsers)

    user_schema = UserSchema(many=True)
    groupUsers = User.get_user_list_from_group_user(groupUsers)
    groupUsers = user_schema.dump(groupUsers)
    group['groupUsers'] = groupUsers

    group_task_schema = GroupTasksSchema(many=True)
    groupTasks = GroupTasks.get_group_tasks_by_group_id(groupId)
    groupTasks = group_task_schema.dump(groupTasks)
    group['groupTasks'] = groupTasks

    return group

# 新しいグループを作成する
def create_new_group(req):
    newGroup = Group.create_group(req)

    return make_response(jsonify({
        "code": 200,
        "createdGroup": create_group_response_model(newGroup),
    }))

# グループの情報を取得
def get_group_info_logic(groupId):
    group = Group.get_group_info_by_groupId(groupId)

    return make_response(jsonify({
        "code": 200,
        "group": create_group_response_model(group),
    }))

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
