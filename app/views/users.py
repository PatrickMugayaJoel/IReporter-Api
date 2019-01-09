""" routes file """

import datetime
from flask import jsonify, request
from flask_jwt import JWT, jwt_required, current_identity
#from app.auth.auth import response_message, token_required, get_token
from app import app
from app.utils.utils import serialize, generate_id
from app.utils.validate_user import Validate_user
from app.models.user import User
from database.users_db import UsersDB


@app.route('/ireporter/api/v2/users', methods=["POST"])
def postuser():

    """ signup """
    try:
        data = request.get_json()
    except:
        return jsonify({"status":400, "error":"No data posted"}), 400

    new_user = User(**data)
    new_user.id = generate_id()
    new_user.registered = datetime.datetime.now().strftime("%Y/%m/%d")
    new_user.isAdmin = False

    user = serialize(new_user)

    validate_user = Validate_user()
    thisuser = validate_user.validate(**user)

    if not thisuser['message'] == 'successfully validated':
        return jsonify({"status":400, "error":thisuser['message']}), 400

    userdb = UsersDB()
    result = userdb.register_user(**user)

    if result=='False':
        print('*****'+str(result))
        return jsonify({"status":400, "error":"User already exists"}), 400

    return jsonify({"status":201,
                    "data":[{
                        "id":new_user.id,
                        "message":"Created User record",
                    }]}), 201


@app.route('/ireporter/api/v2/login', methods=["POST"])
def login():
    """login"""
    if request.is_json:
        username = request.json.get('username')
        password = request.json.get('password')

        userdb = UsersDB()
        credentials = userdb.login(username, password)
        
        if credentials and credentials != 'False':
            return jsonify({'access_token':'access_token', 'status':200}), 200

        payload = {
            'exp': datetime.datetime.utcnow() +
                   datetime.timedelta(days=0, hours=23),
            'user_id': credentials['userId'],
            'is_admin': credentials['is_admin']
        }
        token = jwt.encode(payload, 'trulysKey', algorithm='HS256')

    return jsonify({"error": "Wrong username or password","status":401}), 401


@app.route('/ireporter/api/v2/users', methods=["GET"])
def getusers():

    """ get users """
    if request.method == 'GET':

        userdb = UsersDB()
        users = userdb.users()

        if users and users != 'False':
            return jsonify({"status":200,
                            "data":users
                            }), 200

        return jsonify({"status":404, "error":"No Users found"}), 404

      
