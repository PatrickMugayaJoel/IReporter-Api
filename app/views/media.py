
from flask import jsonify, request, Blueprint
from flask_jwt import jwt_required, current_identity
from database.media_db import MediaDB
from app.utils.utils import get_flag_by_id


media = Blueprint('media_view', __name__)

@media.route('/ireporter/api/v2/red-flags/<int:id>/images', methods=["POST"])
@media.route('/ireporter/api/v2/red-flags/<int:id>/videos', methods=["POST"])
def postmedia(id):

    """ function that handles add media """
    try:
        data = request.get_json()
    except:
        return jsonify({"status":400, "error":"No data posted"}), 400

    if not (data.get('type') and isinstance(data.get('type'), str) and (not data['type'].isspace())):
        return jsonify({"status":400, "error":"type should be a string"}), 400

    if not (data['type'] in ["image","video","comment"]):
        return jsonify({"status":400, "error":"Valid types are video, image, and comment."}), 400

    if not (data.get('input') and isinstance(data.get('input'), str) and (not data['input'].isspace())):
        return jsonify({"status":400, "error":"Input should be a string"}), 400

    if not get_flag_by_id(id):
        return jsonify({"status":404, "error":f"Redflag with id '{id}' not found"}), 404

    data['redflag'] = id

    mediaDB = MediaDB()
    result = mediaDB.add(**data)
    print(result)

    return jsonify({"status":201,
                    "data":[{
                        "id":result['data']['id'],
                        "message":f"{data['type']} successfully added",
                    }]}), 201


@media.route('/ireporter/api/v2/red-flags/<int:id>/<type>', methods=["GET"])
def getmedia(type, id):

    """ funtion to return a list of media """

    type = type.rstrip('s')

    if not get_flag_by_id(id):
        return jsonify({"status":404, "error":f"Redflag with id '{id}' not found"}), 404

    mediaDB = MediaDB()
    result = mediaDB.flag_media(**{'type':type,'redflag':id})
    print(type+'*****'+str(result))
    
    if not result['data']:
        return jsonify({"status":200, "message":"No data to display."})
    
    return jsonify({"status":200,
                    "data":result
                    }), 200

@media.route('/ireporter/api/v2/images/<int:id>', methods=["GET"])
@media.route('/ireporter/api/v2/videos/<int:id>', methods=["GET"])
def getmedia_by_id(id):

    """ function that returns a single image/video by id """

    mediaDB = MediaDB()
    result = mediaDB.check_id(id)

    if not result.get('data'):
        return jsonify({"status":200, "message":"Sorry, resource not found."}), 200

    return jsonify({"status":200,
                    "data":result
                    }), 200

@media.route('/ireporter/api/v2/images/<int:id>', methods=["DELETE"])
@media.route('/ireporter/api/v2/videos/<int:id>', methods=["DELETE"])
@jwt_required()
def delete_media(id):

    """ function to delete a video/image """

    mediaDB = MediaDB()
    medium = mediaDB.check_id(id)

    medium = medium.get('data')

    if not medium:
        return jsonify({"status":404, "error":"Item not found"}), 404

    regflag = get_flag_by_id(medium.get('redflag'))

    if not (current_identity['is_admin'] or (current_identity['userid'] == regflag['createdby']) ):
        return jsonify({"status":401,
                        "data":[{
                            "message":"Sorry! you are not authorised to perform this action.",
                        }]}), 401

    mediaDB.delete(id)

    return jsonify({"status":200,
                    "data":{"id":id,"message":"Record successfully deleted"}
                    }), 200
