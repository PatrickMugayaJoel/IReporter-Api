""" routes file """

import datetime
from flask import jsonify, request
from app import app
from app.utils.utils import serialize, generate_id
from app.utils.validate_user import Validate_user
from app.models.user import User

users = list()

@app.route('/ireporter/api/v2/users', methods=["GET"])
def getusers():

    """ get users """
    if request.method == 'GET':
        if users:
            allusers=serialize(users)
            return jsonify({"status":200,
                            "data":allusers
                            }), 200

        return jsonify({"status":404, "error":"No Users found"}), 404

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

    users.append(new_user)

    return jsonify({"status":201,
                    "data":[{
                        "id":new_user.id,
                        "message":"Created User record",
                    }]}), 201

@app.route('/clearusers')
def clearusers():
    """ clear out data """
    del users[:]
    return 'True', 200

