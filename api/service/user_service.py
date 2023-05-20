from flask import make_response, jsonify
from model.users import User, UserSchema
from model.group_users import GroupUser, GroupUserSchema
from model.groups import Group, GroupSchema
from service.group_task_service import create_group_response_model
import hashlib

def get_user_logic():
    users = User.get_user_list()
    user_schema = UserSchema(many=True)
    return make_response(jsonify({
        'code': 200,
        'users': user_schema.dump(users)
    }))

# 新しいユーザを追加する処理
def create_new_user_logic(req):
    req["password"] = hashlib.sha256(req["password"].encode("utf-8")).hexdigest()
    user = User.create_user(req)
    user_schema = UserSchema()
    return make_response(jsonify({
        'code': 200,
        'newUser': user_schema.dump(user)
    }))

# ユーザ情報を更新する処理
def update_user_logic(req, userId):
    if "userName" in req:
        user = User.change_user_name(str(req["userName"]), userId)
    if "password" in req:
        req["password"] = hashlib.sha256(req["password"].encode("utf-8")).hexdigest()
        user = User.change_user_password(req["password"], userId)
    user_schema = UserSchema()
    return make_response(jsonify({
        'code': 200,
        'users': user_schema.dump(user)
    }))

# ログインの認証をする処理
def user_login_rogic(req):
    req['userId'] = int(req['userId'])
    req['password'] = hashlib.sha256(req["password"].encode("utf-8")).hexdigest()
    user = User.check_user(req)
    print(user)
    if user:
        user_schema = UserSchema()
        return make_response(jsonify({
            'code': 200,
            'user': user_schema.dump(user[0]),
            'token': 'TEST_TOKEN',
        }))
    else :
        return make_response(jsonify({
            'code': 406,
            'msg': 'ログインに失敗しました'
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
    GroupUser.user_join_group(req['groupId'], userId)

    responseGroup = Group.get_group_info_by_groupId(req['groupId'])
    return make_response(jsonify({
        "code": 200,
        "group": create_group_response_model(responseGroup),
    }))