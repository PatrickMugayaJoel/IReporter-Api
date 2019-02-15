
import datetime
from flask import jsonify, request, Blueprint
from flask_jwt_extended import jwt_required, get_jwt_identity
from flasgger.utils import swag_from
from app.utils.validate_user import Validate_user
from app.utils.utils import serialize
from app.models.user import User
from database.users_db import UsersDB

userdb = UsersDB()
userdb.default_users()

users_view = Blueprint('users_view', __name__)


@users_view.route('/ireporter/api/v2/auth/signup', methods=["POST"])
@swag_from('../docs/users/signup.yml')
def postuser(): 

    """ function to add a user """
    try: 
        data = request.get_json()
    except Exception: 
        return jsonify({"status": 400, "error": "No data posted"}), 400

    new_user = User(**data)
    new_user.registered = datetime.datetime.now().strftime("%Y/%m/%d")
    new_user.is_admin = False

    user = serialize(new_user)

    validate_user = Validate_user()
    theuser = validate_user.validate(**user)

    if not theuser['message'] == 'successfully validated': 
        return jsonify({"error": theuser['message'], "status": 400}), 400

    result = userdb.register_user(**user)

    if not result['status']:
        return jsonify({"status": 400, "error": "User already exists"}), 400

    return jsonify({"status": 201,
                    "data": [{
                        "user": userdb.check_id(result['data']['userid']),
                    }]}), 201


@users_view.route('/ireporter/api/v2/users', methods=["GET"])
@jwt_required
@swag_from('../docs/users/getusers.yml')
def getusers(): 

    """ function to get all users """

    if not get_jwt_identity()['is_admin']: 
        return jsonify({"status": 401,
                        "data": [{
                            "message": "Sorry! Access restricted to administrators.",
                        }]}), 401

    users = userdb.users()

    return jsonify({"status": 200,
                    "data": users
                    }), 200

  
@users_view.route('/ireporter/api/v2/users/<int:id>', methods=["GET"])
@jwt_required
@swag_from('../docs/users/getauser.yml')
def getauser(id): 

    """ function to get a user by id """

    if not (get_jwt_identity()['is_admin'] or (get_jwt_identity()['userid'] == id)): 
        return jsonify({"error": "Sorry! Access denied.",
                        }), 401

    user = userdb.check_id(id)

    if user and user != 'False': 
        return jsonify({"status": 200,
                        "data": [user]
                        }), 200

    return jsonify({"status": 404, "error": "User not found"}), 404

@users_view.route('/ireporter/api/v2/users/<int:id>', methods=["PUT"])
@jwt_required
@swag_from('../docs/users/updateuser.yml')
def updateuser(id): 
    """ function to update user data """

    if not (get_jwt_identity()['is_admin'] or (get_jwt_identity()['userid'] == id)): 
        return jsonify({"status": 401,
                        "data": [{
                            "message": "Sorry! Access denied.",
                        }]}), 401

    try: requestdata = request.get_json()
    except Exception: 
        return jsonify({"error": "No data posted", "status": 400}), 400

    user = userdb.check_id(id)
    if not user or user == 'False': 
        return jsonify({"status": 404, "error": "User not found"}), 404

    for key in requestdata: 
        user[key] = requestdata[key]

    user['id'] = user['userid']
    user['registered'] = 'date'

    validate_user = Validate_user()
    thisuser = validate_user.validate(**user)

    if not thisuser['message'] == 'successfully validated': 
        return jsonify({"status": 400, "error": thisuser['message']}), 400

    result = userdb.update(**user)

    if result=='False': 
        return jsonify({"status": 400, "error": "User update failed"}), 400

    return jsonify({"status": 200,
                    "data": [{
                        "id": id,
                        "message": "Updated User record",
                    }]}), 200

