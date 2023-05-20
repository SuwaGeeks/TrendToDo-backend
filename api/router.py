from flask import Blueprint, request
from controller import user_controller
from controller import personal_task_controller
from controller import group_task_controller
from logging import config
import json
from json import load
import auth
import logger

# Generate Router Instance
router = Blueprint('router', __name__)

# Read Logging Configuration
with open("./config/logging.json", "r", encoding="utf-8") as f:
  config.dictConfig(load(f))

@router.route("/", methods=['GET'])
@logger.http_request_logging
@auth.requires_auth
def hello_world():
  return "Hello World!!"

###########################
# User : ユーザに関わるAPI
###########################
# 新しいユーザの作成
@router.route("/api/user", methods=['POST'])
@logger.http_request_logging
@auth.requires_auth
def post_user():
  return user_controller.create_new_user(request.json)

# ユーザデータの更新
@router.route("/api/users/<userId>", methods=['PATCH'])
@logger.http_request_logging
@auth.requires_auth
def patch_users_by_userId(userId):
  return user_controller.update_user_info(request.json, int(userId))

# ログイン用のエンドポイント
@router.route("/api/login", methods=['POST'])
@logger.http_request_logging
@auth.requires_auth
def post_login():
  return user_controller.login_user(request.json)

# ユーザの参加しているグループの一覧を取得するAPI
@router.route("/api/user/<userId>/group", methods=['GET'])
@logger.http_request_logging
@auth.requires_auth
def get_user_group_by_userId(userId):
  return user_controller.get_user_group_by_userId(userId)

# 新しいグループに参加するAPI
@router.route("/api/user/<userId>/group", methods=['POST'])
@logger.http_request_logging
@auth.requires_auth
def post_user_group(userId):
  return user_controller.post_user_group(request.json, userId)


##################################
# UserTask : 個人タスクに関わるAPI
##################################
# 個人タスクの一覧を取得
@router.route("/api/user/<userId>/tasks/user", methods=['GET'])
@logger.http_request_logging
@auth.requires_auth
def get_personal_tasks(userId):
  return personal_task_controller.get_personal_task_list(userId)

# 新しい個人タスクの追加
@router.route("/api/user/<userId>/tasks/user", methods=['POST'])
@logger.http_request_logging
@auth.requires_auth
def post_personal_task(userId):
  return personal_task_controller.post_personal_task(request.json, userId)

# タスクIDで指定したタスクの情報を取得
@router.route("/api/user/<userId>/tasks/user/<taskId>", methods=['GET'])
@logger.http_request_logging
@auth.requires_auth
def get_personl_task_by_taskId(userId, taskId):
  return personal_task_controller.get_personal_task_by_taskId(userId, taskId)

# タスクIDで指定したタスクの内容を変更
@router.route("/api/user/<userId>/tasks/user/<taskId>", methods=['PUT'])
@logger.http_request_logging
@auth.requires_auth
def put_personl_task_by_taskId(userId, taskId):
  return personal_task_controller.put_personal_task_by_taskId(request.json, taskId)

# タスクIDで指定したタスクを削除
@router.route("/api/user/<userId>/tasks/user/<taskId>", methods=['DELETE'])
@logger.http_request_logging
@auth.requires_auth
def delete_personl_task_by_taskId(userId, taskId):
  return personal_task_controller.delete_personal_task_by_taskId(taskId)#名前の重複?

##################################
# GroupTask : グループタスクに関わるAPI
##################################
# ユーザIDで指定したユーザが所属しているグループの全てのタスクを取得
@router.route("/api/user/<userId>/tasks/group", methods=['GET'])#group_tasks.pyに存在しない
@logger.http_request_logging
@auth.requires_auth
def get_group_task_by_userId(userId):
  return group_task_controller.get_all_group_task_by_userId(userId)

# 新しいグループを作成するAPI
@router.route("/api/group", methods=['POST'])#group_tasks.pyに存在しない
@logger.http_request_logging
@auth.requires_auth
def post_new_group():
  return group_task_controller.post_new_group(request.json)

# グループの情報を取得するAPI
@router.route("/api/group/<groupId>", methods=['GET'])#group_tasks.pyに存在しない
@logger.http_request_logging
@auth.requires_auth
def get_group_info_by_userId(groupId):
  return group_task_controller.get_group_info_by_userId(int(groupId))


# グループIDで指定したグループのタスク一覧を取得
@router.route("/api/group/<groupId>/tasks",methods=['GET'])
@logger.http_request_logging
@auth.requires_auth
def get_group_task_by_groupId(groupId):
  return group_task_controller.get_group_task_list_by_groupId(groupId)

# グループIDで指定したグループに新しいタスクを追加
@router.route("/api/group/<groupId>/tasks",methods=['POST'])
@logger.http_request_logging
@auth.requires_auth
def post_group_task(groupId):
  return group_task_controller.post_group_task(request.json)

#指定したグループの指定したタスクの情報を取得
@router.route("/api/group/<groupId>/tasks/<taskId>",methods=['GET'])
@logger.http_request_logging
@auth.requires_auth
def get_group_task_by_taskId(groupId, taskId):
  return group_task_controller.get_group_task_info_by_taskId(taskId)

#指定したグループの指定したタスクの内容を変更
@router.route("/api/group/<groupId>/tasks<taskId>",methods=['PUT'])
@logger.http_request_logging
@auth.requires_auth
def put_group_task_by_taskId(groupId, taskId):
  return group_task_controller.put_group_task_info(request.json, taskId)
  
#指定したグループの指定したタスクを削除
@router.route("/api/group/<groupId>/tasks/<taskId>",methods=['DELETE'])
@logger.http_request_logging
@auth.requires_auth
def delete_group_task_by_taskId(groupId, taskId):
  return group_task_controller.delete_group_task(taskId)


##################################
# SubmitTask : タスクを消化するAPI
##################################
#個人タスクを消化する
@router.route("/api/submit/user/<taskId>",methods=['POST'])
@logger.http_request_logging
@auth.requires_auth
def post_submit_personal_task(taskId):
  return personal_task_controller.submit_personal_task(taskId)

#グループタスクを消化する
@router.route("/api/submit/group/<taskId>",methods=['POST'])
@logger.http_request_logging
@auth.requires_auth
def post_submit_group_task(taskId):
  return group_task_controller.submit_group_task(taskId)


##################################
# Admin : 管理用のAPI
##################################
@router.route("/api/getUserList", methods=['GET'])
@logger.http_request_logging
@auth.requires_auth
def api_v1_users_get_user_list():
  return user_controller.get_user()

@router.after_request
def after_request(response):
  # response.headers.add('Access-Control-Allow-Origin', '*')
  response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
  response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
  return response