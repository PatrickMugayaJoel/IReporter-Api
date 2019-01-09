
from flask_jwt import JWT

jwt = JWT()

@jwt.authentication_handler
def authenticate(username, password):
    user = username_table.get(username, None)
    if user and safe_str_cmp(user.password.encode('utf-8'), password.encode('utf-8')):
        return user

@jwt.identity_handler
def identity(payload):
    user_id = payload['identity']
    return userid_table.get(user_id, None)

@jwt.error_handler
def error_handler(e):
    return "Something bad happened", 400


