
import datetime
from flask import jsonify, request
from app import app
from app.utils.utils import serialize, generate_id
from app.utils.validate_redflag import Validate_redflag
from app.models.redflag import Redflag
from database.redflags_db import RedflagsDB


@app.route('/ireporter/api/v2/red-flags', methods=["GET"])
def getredflags():

    """ get red-flags """
    if request.method == 'GET':

        regflagdb = RedflagsDB()
        regflags = regflagdb.regflags()

        if regflags and regflags != 'False':
            return jsonify({"status":200,
                            "data":regflags
                            }), 200
        
        return jsonify({"status":"404", "error":"No redflags found"}), 404

@app.route('/ireporter/api/v2/red-flags', methods=["POST"])
def postredflag():

    """ add a red flag """
    try:
        data = request.get_json()
    except:
        return jsonify({"status":400, "error":"No data was posted"}), 400

    new_red_flag = Redflag(**data)


    regflagdb = RedflagsDB()
    
    title = regflagdb.check_title(new_red_flag.title)
    
    if title and title != 'False':
        return jsonify({"status":400, "error":"Incident already exists"}), 400
    
    new_red_flag.id = generate_id()
    new_red_flag.createdOn = datetime.datetime.now().strftime("%Y/%m/%d")
    new_red_flag.createdBy = 20190107093147712
    new_red_flag.status = 'under investigation'

    validate_redflag = Validate_redflag()
    thisredflag = validate_redflag.validate(**serialize(new_red_flag))

    if thisredflag['message'] != 'successfully validated':
        return jsonify({"status":400, "error":thisredflag['message']}), 400

    is_saved = regflagdb.register_flag(**serialize(new_red_flag))

    if is_saved == 'True':
        return jsonify({"status":201,
                        "data":[{
                            "id":new_red_flag.id,
                            "message":"Created red-flag Record"
                            }]
                        }), 201
    else:
        return jsonify({"status":400, "error":'Data not saved. sorry'}), 400



def get_flag_by_id(id):
    """ get flag by id """

    regflagdb = RedflagsDB()
    regflag = regflagdb.check_flag(id)

    if regflag and regflag != 'False':
        return regflag
    else:
        regflag = None
        return regflag

@app.route('/ireporter/api/v2/red-flags/<int:id>', methods=["GET"])
def get(id):

    regflag = get_flag_by_id(id)
    
    if regflag:
        return jsonify({"status":200,
                        "data":regflag
                        }), 200

    return jsonify({"status":404, "error":"Redflag not found"}), 404

@app.route('/ireporter/api/v2/red-flags/<int:id>', methods=["DELETE"])
def delete(id):

    regflag = get_flag_by_id(id)

    if regflag:
        regflagdb = RedflagsDB()
        if regflagdb.delete(id):
            return jsonify({"status":200,
                            "message":"Deleted red-flag Record"
                            }), 200
        else:
            return jsonify({"status":400, "error":"Record could not be deleted"}), 400

    return jsonify({"status":404, "error":"Redflag not found"}), 404

@app.route('/ireporter/api/v2/red-flags/<int:id>', methods=["PUT"])
def put(id):

    regflag = get_flag_by_id(id)
        
    try: data = request.get_json()
    except: return jsonify({"status":400, "error":"No data was posted"}), 400

    if not regflag:
        return jsonify({"status":404, "error":"Redflag not found"}), 404

    for key in data:
        regflag[key] = data[key]

    regflag['id'] = regflag['flag_id']
    regflag['createdOn'] = str(regflag['createdon'])
    regflag['createdBy'] = regflag['createdby']

    validate_redflag = Validate_redflag()
    validited = validate_redflag.validate(**regflag)

    if validited['message'] != 'successfully validated':
        return jsonify({"status":400, "error":validited['message']}), 400

    regflagdb = RedflagsDB()
    if regflagdb.update(**regflag) == 'True':
        return jsonify({"status":200,
                        "message":"Updated red-flag Record"
                        }), 200
    else:
        return jsonify({"status":400, "error":"sorry. Flag could not be updated"}), 400
