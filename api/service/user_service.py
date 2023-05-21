from flask import make_response, jsonify
from model.users import User, UserSchema
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
    req['userName'] = req['userName']
    req['password'] = hashlib.sha256(req["password"].encode("utf-8")).hexdigest()
    user = User.check_user(req)
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
    