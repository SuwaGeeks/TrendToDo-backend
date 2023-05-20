from service.user_service import *

def get_user():
  return get_user_logic()

def create_new_user(reqBody):
  return create_new_user_logic(reqBody)

def update_user_info(reqBody, userId):
  return update_user_logic(reqBody, userId)

def login_user(reqBody):
  return user_login_rogic(reqBody)

# ユーザの参加しているグループの一覧を取得するAPI
def get_user_group_by_userId(userId):
  return get_user_group_list_logic_by_userId(userId)

# 新しいグループに参加するAPI
def post_user_group(reqBody, userId):
  return join_new_group_logic(reqBody, userId)