
from flask import jsonify, request, Blueprint
from database.media_db import MediaDB
from app.views.redflags import get_flag_by_id


media = Blueprint('media_view', __name__)

@media.route('/ireporter/api/v2/red-flags/<int:id>/images', methods=["POST"])
@media.route('/ireporter/api/v2/red-flags/<int:id>/videos', methods=["POST"])
@media.route('/ireporter/api/v2/red-flags/<int:id>/comments', methods=["POST"])
def postmedia(id):

    """ add media """
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

    if not result['status']:
        print('***** in post '+str(result['message']))
        return jsonify({"status":400, "error":"Sorry resource not saved"}), 400

    return jsonify({"status":201,
                    "data":[{
                        "id":result['data']['id'],
                        "message":f"{data['type']} successfully added",
                    }]}), 201


@media.route('/ireporter/api/v2/red-flags/<int:id>/images', methods=["GET"])
def getimages(id):
    return getmedia('image', id)

@media.route('/ireporter/api/v2/red-flags/<int:id>/videos', methods=["GET"])
def getvideos(id):
    return getmedia('video', id)

@media.route('/ireporter/api/v2/red-flags/<int:id>/comments', methods=["GET"])
def getcomments(id):
    return getmedia('comment', id)

def getmedia(type, id):

    if not get_flag_by_id(id):
        return jsonify({"status":404, "error":f"Redflag with id '{id}' not found"}), 404

    mediaDB = MediaDB()
    result = mediaDB.flag_media(**{'type':type,'redflag':id})
    print(str(result))
    
    if not result['status']:
        print('***** in post '+str(result['message']))
        return jsonify({"status":400, "error":"Sorry resource not saved"})
    elif not result['data']:
        return jsonify({"status":200, "message":"No data to display."})

    return jsonify({"status":200,
                    "data":result
                    }), 200

@media.route('/ireporter/api/v2/red-flags/medium/<int:id>', methods=["GET"])
@media.route('/ireporter/api/v2/red-flags/images/<int:id>', methods=["GET"])
@media.route('/ireporter/api/v2/red-flags/videos/<int:id>', methods=["GET"])
@media.route('/ireporter/api/v2/red-flags/comments/<int:id>', methods=["GET"])
def getmedia_by_id(id):

    mediaDB = MediaDB()
    result = mediaDB.check_id(id)

    if not result['status']:
        print('***** in post '+str(result['message']))
        return jsonify({"status":400, "error":"Sorry, request not successful try again"}), 400
    elif not result['data']:
        return jsonify({"status":200, "message":"Sorry, resource not found."}), 200

    return jsonify({"status":200,
                    "data":result
                    }), 200

@media.route('/ireporter/api/v2/red-flags/<int:flag_id>/comments/<int:id>', methods=["PUT"])
def update_comment(flag_id, id):

    try:
        data = request.get_json()
    except:
        return jsonify({"status":400, "error":"No data posted"}), 400

    if not (data.get('comment') and isinstance(data.get('comment'), str) and (not data['comment'].isspace())):
        return jsonify({"status":400, "error":"Comment should be a string"}), 400

    data['id'] = id

    mediaDB = MediaDB()
    result = mediaDB.update(**data)

    if not result['status']:
        print('***** in post '+str(result['message']))
        return jsonify({"status":400, "error":"Sorry, request not successful try again"}), 400
    elif not result['data']:
        return jsonify({"status":200, "message":"Sorry, resource not found."}), 200

    return jsonify({"status":200,
                    "data":{"id":result['data']['id'], "message":"record update was successfull"}
                    }), 200

@media.route('/ireporter/api/v2/red-flags/<int:flag_id>/images/<int:id>', methods=["DELETE"])
@media.route('/ireporter/api/v2/red-flags/<int:flag_id>/videos/<int:id>', methods=["DELETE"])
@media.route('/ireporter/api/v2/red-flags/<int:flag_id>/comments/<int:id>', methods=["DELETE"])
def delete_media(flag_id, id):

    mediaDB = MediaDB()
    result = mediaDB.delete(id)

    if not result['status']:
        print('***** in post '+str(result['message']))
        return jsonify({"status":400, "error":"Sorry, request not successful try again"}), 400

    return jsonify({"status":200,
                    "data":{"id":id,"message":"Record successfully deleted"}
                    }), 200
