from flask import make_response, jsonify
from model.groups import Group, GroupSchema
from model.group_users import GroupUser, GroupUserSchema
from model.group_tasks import GroupTasks, GroupTasksSchema
from model.group_task_logs import GroupTaskLog, GroupTaskLogSchema
from model.users import User, UserSchema

#ユーザIDで指定したユーザが所属しているグループのすべてのタスクを取得
def get_all_group_task_by_userId_logic(userId):
    # 所属しているすべてグループを取得
    group_users = GroupUser.get_all_group_by_user_id(userId)
    group_user_schema = GroupUserSchema(many=True)
    group_users = group_user_schema.dump(group_users)

    group_tasks = GroupTasks.get_group_tasks_by_group_user(group_users)
    group_tasks_schema = GroupTasksSchema(many=True)
    return make_response(jsonify({
        "code": 200,
        "group": group_tasks_schema.dump(group_tasks),
    }))

# ユーザの参加しているグループの一覧を取得する処理
def get_user_group_list_logic_by_userId(userId):
    group_users = GroupUser.get_all_group_by_user_id(userId)
    group_user_schema = GroupUserSchema(many=True)
    group_users = group_user_schema.dump(group_users)

    group_schema = GroupSchema(many=True)
    groups = Group.get_groupList_from_group_user(group_users)

    return make_response(jsonify({
        "code": 200,
        "group": group_schema.dump(groups)
    }))

# 新しいグループに参加する処理
def join_new_group_logic(req, userId):
    targetGroup = Group.get_group_by_groupName(req['groupName'])
    if not targetGroup:
        return make_response(jsonify({
            "code": 404,
            "message": "指定したグループ名のグループが見つかりません"
        }))

    req['groupId'] = targetGroup[0].groupId

    GroupUser.user_join_group(req['groupId'], userId)

    responseGroup = Group.get_group_info_by_groupId(req['groupId'])
    return make_response(jsonify({
        "code": 200,
        "group": create_group_response_model(responseGroup),
    }))

# グループのレスポンスモデルを作成する関数
def create_group_response_model(group):
    group_schema = GroupSchema()
    group = group_schema.dump(group)
    # print(group)
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
    for i in range(len(groupTasks)):
        groupTasks[i] = create_group_task_response_model(groupTasks[i])
    group['groupTasks'] = groupTasks

    return group

# グループタスクのレスポンスモデルを作成する関数
def create_group_task_response_model(group_task):
    groupTaskId = group_task['taskId']

    weight = GroupTaskLog.calc_group_task_weight_by_task_id(groupTaskId)[0][0] or 0.
    taskTime = GroupTaskLog.calc_group_task_time_by_task_id(groupTaskId)[0][0] or 0.

    group_task['taskWeight'] = float(weight)
    group_task['meanTime'] = float(taskTime)
    
    return group_task

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
def submit_group_task_logic(req, taskId):
    targetTask = GroupTasks.get_group_task_by_task_id(taskId)

    req['taskId'] = taskId
    req['groupId'] = targetTask.taskGroupId
    GroupTaskLog.add_group_task_log(req)

    task = GroupTasks.get_group_task_by_task_id(taskId)
    group_task_schema=GroupTasksSchema()
    group_task = group_task_schema.dump(task)
    group_task = create_group_task_response_model(group_task)

    return make_response(jsonify({
        "code": 200,
        "task": group_task
    }))
