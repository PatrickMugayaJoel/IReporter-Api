
import datetime
from flask import jsonify, request, Blueprint
from flask_jwt import jwt_required, current_identity
from flasgger.utils import swag_from
from app.utils.utils import serialize, get_flag_by_id
from app.utils.validate_redflag import Validate_redflag
from app.models.redflag import Redflag
from database.incidents_db import IncidentsDB
from database.media_db import MediaDB

redflags_view = Blueprint('redflags_view', __name__)
incidents_db = IncidentsDB()
mediaDB = MediaDB()

@redflags_view.route('/ireporter/api/v2/<type>', methods=["GET"])
@swag_from('../docs/redflags/getflags.yml')
def getredflags(type):

    """ function to get red-flags """

    if not (type in ["red-flags","interventions"]):
        return jsonify({"status":"404", "error":"Invalid URL"}), 404
    
    regflags = incidents_db.regflags(type.rstrip('s'))

    if not (regflags and regflags != 'False'):
        return jsonify({"status":"404", "error":f"No {type} found"}), 404

    for flag in regflags:
        flag['Video'] = [item[0] for item in mediaDB.flag_media(**{'type':'video','redflag':flag['flag_id']}).get('data',[])]
        flag['Image'] = [item[0] for item in mediaDB.flag_media(**{'type':'image','redflag':flag['flag_id']}).get('data',[])]

    return jsonify({"status":200,
                    "data":regflags
                    }), 200
    

@redflags_view.route('/ireporter/api/v2/<type>', methods=["POST"])
@jwt_required()
@swag_from('../docs/redflags/postflag.yml')
def postredflag(type):

    """ function to add a red flag """

    if not (type in ["red-flags","interventions"]):
        return jsonify({"status":"404", "error":"Invalid URL"}), 404

    try:
        data = request.get_json()
    except:
        return jsonify({"status":400, "error":"No data was posted"}), 400

    new_red_flag = Redflag(**data)
    
    title = incidents_db.check_title(new_red_flag.title)
    
    if title and title != 'False':
        return jsonify({"status":400, "error":"Incident already exists"}), 400

    new_red_flag.createdon = datetime.datetime.now().strftime("%Y/%m/%d")
    new_red_flag.createdby = current_identity['userid']
    new_red_flag.status = 'pending'
    new_red_flag.type = type.rstrip('s')

    validate_redflag = Validate_redflag()
    thisredflag = validate_redflag.validate(**serialize(new_red_flag))

    if thisredflag['message'] != 'successfully validated':
        return jsonify({"status":400, "error":thisredflag['message']}), 400

    result = incidents_db.register_flag(**serialize(new_red_flag))

    if not result['status']:
        return jsonify({"status":400, "error":result['error']}), 400


    return jsonify({"status":201,
                    "data":[{
                        "id":result['data']['flag_id'],
                        "message":f"Created {type.rstrip('s')} Record"
                        }]
                    }), 201

@redflags_view.route('/ireporter/api/v2/<type>/<int:id>', methods=["GET"])
@swag_from('../docs/redflags/getaflag.yml')
def get(type, id):

    """ function to get a single redflag by id """

    if not (type in ["red-flags","interventions"]):
        return jsonify({"status":"404", "error":"Invalid URL"}), 404

    regflag = get_flag_by_id(id)
    
    if regflag and regflag != 'False':

        regflag['Video'] = [item[0] for item in mediaDB.flag_media(**{'type':'video','redflag':regflag['flag_id']}).get('data',[])]
        regflag['Image'] = [item[0] for item in mediaDB.flag_media(**{'type':'image','redflag':regflag['flag_id']}).get('data',[])]

        return jsonify({"status":200,
                        "data":regflag
                        }), 200

    return jsonify({"status":404, "error":f"{type.rstrip('s')} not found"}), 404

@redflags_view.route('/ireporter/api/v2/<type>/<int:id>', methods=["DELETE"])
@jwt_required()
@swag_from('../docs/redflags/deleteaflag.yml')
def delete(type, id):

    """ function to delete a redflag """

    regflag = get_flag_by_id(id)

    if not (current_identity['is_admin'] or (current_identity['userid'] == regflag['createdby']) ):
        return jsonify({"status":401,
                        "error":"Sorry! you are not authorised to perform this action.",
                        }), 401

    if regflag:
        incidents_db.delete(id)
        return jsonify({"status":200,
                        "data":[{
                        "message":f"{type.rstrip('s')} record has been deleted",
                        "id": id
                        }]
                        }), 200

    return jsonify({"status":404, "error":f"{type.rstrip('s')} not found"}), 404

@redflags_view.route('/ireporter/api/v2/<type>/<int:id>/<attribute>', methods=["PATCH"])
@jwt_required()
@swag_from('../docs/redflags/patchaflag.yml')
def patch(type, id, attribute):

    """ function to update a redflag """

    if not (type in ["red-flags","interventions"]):
        return jsonify({"status":"404", "error":"Invalid URL"}), 404

    if not (attribute in ["comment", "location", "status"]):
        return jsonify({"status":"404", "error":"Invalid URL"}), 404

    try: data = request.get_json()
    except: return jsonify({"status":400, "error":"No data was posted"}), 400

    if attribute == "status" and not (data.get('status') in ['under investigation', 'rejected', 'resolved']):
        return jsonify({"status":400, "error":"Invalid status"}), 400

    regflag = get_flag_by_id(id)

    if not regflag:
        return jsonify({"status":404, "error":f"{type.rstrip('s')} not found"}), 404

    if attribute == "status" and not current_identity['is_admin']:
        return jsonify({"status":401,
                        "error":"Sorry! only administrators allowed.",
                        }), 401
    if not (current_identity['is_admin'] or (current_identity['userid'] == regflag['createdby']) ):
        return jsonify({"status":401,
                        "error":"Sorry! you are not authorised to perform this action.",
                        }), 401

    regflag[attribute] = data[attribute]
    
    regflag['createdon'] = regflag['createdon'].strftime("%Y/%m/%d")
    regflag['id'] = regflag['flag_id']

    validate_redflag = Validate_redflag()
    validited = validate_redflag.validate(**regflag)

    if validited['message'] != 'successfully validated':
        return jsonify({"status":400, "error":validited['message']}), 400

    if incidents_db.update(**regflag) == 'True':
        return jsonify({"status":200,
                        "data":[{
                        "message":f"Updated {type.rstrip('s')} record's {attribute}",
                        "id": id
                        }]
                        }), 200
