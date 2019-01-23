
import datetime
from flask import jsonify, request, Blueprint
from flask_jwt import jwt_required, current_identity
from app.utils.utils import serialize, generate_id, get_flag_by_id
from app.utils.validate_redflag import Validate_redflag
from app.models.redflag import Redflag
from database.redflags_db import RedflagsDB
from database.media_db import MediaDB

redflags_view = Blueprint('redflags_view', __name__)
regflagdb = RedflagsDB()
mediaDB = MediaDB()

@redflags_view.route('/ireporter/api/v2/<type>', methods=["GET"])
def getredflags(type):

    """ get red-flags """

    if not (type in ["red-flags","interventions"]):
        return jsonify({"status":"404", "error":"Invalid URL"}), 404
    
    regflags = regflagdb.regflags(type.rstrip('s'))

    if regflags and regflags != 'False':

        regflags[0]['Video'] = mediaDB.flag_media(**{'type':'video','redflag':regflags[0]['flag_id']})['data']
        regflags[0]['Image'] = mediaDB.flag_media(**{'type':'image','redflag':regflags[0]['flag_id']})['data']

        return jsonify({"status":200,
                        "data":regflags
                        }), 200
    
    return jsonify({"status":"404", "error":f"No {type} found"}), 404

@redflags_view.route('/ireporter/api/v2/<type>', methods=["POST"])
@jwt_required()
def postredflag(type):

    """ add a red flag """

    if not (type in ["red-flags","interventions"]):
        return jsonify({"status":"404", "error":"Invalid URL"}), 404

    try:
        data = request.get_json()
    except:
        return jsonify({"status":400, "error":"No data was posted"}), 400

    new_red_flag = Redflag(**data)
    
    title = regflagdb.check_title(new_red_flag.title)
    
    if title and title != 'False':
        return jsonify({"status":400, "error":"Incident already exists"}), 400
    
    new_red_flag.id = generate_id()
    new_red_flag.createdon = datetime.datetime.now().strftime("%Y/%m/%d")
    new_red_flag.createdby = current_identity['userid']
    new_red_flag.status = 'under investigation'
    new_red_flag.type = type.rstrip('s')

    validate_redflag = Validate_redflag()
    thisredflag = validate_redflag.validate(**serialize(new_red_flag))

    if thisredflag['message'] != 'successfully validated':
        return jsonify({"status":400, "error":thisredflag['message']}), 400

    regflagdb.register_flag(**serialize(new_red_flag))

    return jsonify({"status":201,
                    "data":[{
                        "id":new_red_flag.id,
                        "message":f"Created {type.rstrip('s')} Record"
                        }]
                    }), 201

@redflags_view.route('/ireporter/api/v2/<type>/<int:id>', methods=["GET"])
def get(type, id):

    if not (type in ["red-flags","interventions"]):
        return jsonify({"status":"404", "error":"Invalid URL"}), 404

    regflag = get_flag_by_id(id)
    
    if regflag and regflag != 'False':

        regflag[0]['Video'] = mediaDB.flag_media(**{'type':'video','redflag':regflag[0]['flag_id']})['data']
        regflag[0]['Image'] = mediaDB.flag_media(**{'type':'image','redflag':regflag[0]['flag_id']})['data']

        return jsonify({"status":200,
                        "data":regflag
                        }), 200

    return jsonify({"status":404, "error":f"{type.rstrip('s')} not found"}), 404

@redflags_view.route('/ireporter/api/v2/<type>/<int:id>', methods=["DELETE"])
@jwt_required()
def delete(type, id):

    regflag = get_flag_by_id(id)

    if not (current_identity['is_admin'] or (current_identity['userid'] == regflag['createdby']) ):
        return jsonify({"status":401,
                        "error":"Sorry! you are not authorised to perform this action.",
                        }), 401

    if regflag:
        regflagdb.delete(id)
        return jsonify({"status":200,
                        "data":[{
                        "message":f"{type.rstrip('s')} record has been deleted",
                        "id": id
                        }]
                        }), 200

    return jsonify({"status":404, "error":f"{type.rstrip('s')} not found"}), 404

@redflags_view.route('/ireporter/api/v2/<type>/<int:id>/<atribute>', methods=["PATCH"])
@jwt_required()
def patch(type, id, atribute):

    if not (type in ["red-flags","interventions"]):
        return jsonify({"status":"404", "error":"Invalid URL"}), 404

    if not (atribute in ["comment", "location", "status"]):
        return jsonify({"status":"404", "error":"Invalid URL"}), 404

    try: data = request.get_json()
    except: return jsonify({"status":400, "error":"No data was posted"}), 400

    regflag = get_flag_by_id(id)

    if not regflag:
        return jsonify({"status":404, "error":f"{type.rstrip('s')} not found"}), 404

    print(regflag)
    if atribute == "status" and not current_identity['is_admin']:
        return jsonify({"status":401,
                        "error":"Sorry! only administrators allowed.",
                        }), 401
    if not (current_identity['is_admin'] or (current_identity['userid'] == regflag['createdby']) ):
        return jsonify({"status":401,
                        "error":"Sorry! you are not authorised to perform this action.",
                        }), 401

    regflag[atribute] = data[atribute]
    
    regflag['createdon'] = regflag['createdon'].strftime("%Y/%m/%d")
    regflag['id'] = regflag['flag_id']

    validate_redflag = Validate_redflag()
    validited = validate_redflag.validate(**regflag)

    if validited['message'] != 'successfully validated':
        return jsonify({"status":400, "error":validited['message']}), 400

    if regflagdb.update(**regflag) == 'True':
        return jsonify({"status":200,
                        "data":[{
                        "message":f"Updated {type.rstrip('s')} record's {atribute}",
                        "id": id
                        }]
                        }), 200
