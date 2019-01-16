
from flask import jsonify, request, Blueprint
from database.media import MediaDB


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

    if not (data['type'] and isinstance(data['type'], str)):
        return jsonify({"status":400, "error":"type should be a string"}), 400

    if not (data['input'] and isinstance(data['data'], str)):
        return jsonify({"status":400, "error":"Input should be a string"}), 400

    data['redflag'] = id

    mediaDB = MediaDB()
    result = mediaDB.add(**data)

    if not result['status']:
        print('***** in post '+str(result['message']))
        return jsonify({"status":400, "error":"Sorry resource not saved"}), 400

    return jsonify({"status":201,
                    "data":[{
                        "id":result['id'],
                        "message":f"{data['type']} successfuly added",
                    }]}), 201


@media.route('/ireporter/api/v2/red-flags/<int:id>/images', methods=["GET"])
def getimages(id):
    result = getmedia('image', id)
    return result,result['status']

@media.route('/ireporter/api/v2/red-flags/<int:id>/videos', methods=["GET"])
def getvideos(id):
    result = getmedia('video', id)
    return result,result['status']

@media.route('/ireporter/api/v2/red-flags/<int:id>/comments', methods=["GET"])
def getcomments(id):
    result = getmedia('comment', id)
    return result,result['status']

def getmedia(type, id):

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

@media.route('/ireporter/api/v2/red-flags/medium/<int:id>', methods=["PUT"])
@media.route('/ireporter/api/v2/red-flags/images/<int:id>', methods=["PUT"])
@media.route('/ireporter/api/v2/red-flags/videos/<int:id>', methods=["PUT"])
@media.route('/ireporter/api/v2/red-flags/comments/<int:id>', methods=["PUT"])
def update_medium(id):

    try:
        data = request.get_json()
    except:
        return jsonify({"status":400, "error":"No data posted"}), 400

    if not (data['input'] and isinstance(data['data'], str)):
        return jsonify({"status":400, "error":"Input should be a string"}), 400

    mediaDB = MediaDB()
    result = mediaDB.update(**data)

    if not result['status']:
        print('***** in post '+str(result['message']))
        return jsonify({"status":400, "error":"Sorry, request not successful try again"}), 400
    elif not result['data']:
        return jsonify({"status":200, "message":"Sorry, resource not found."}), 200

    return jsonify({"status":200,
                    "data":{"id":result['id'], "message":"record update was successfull"}
                    }), 200

@media.route('/ireporter/api/v2/red-flags/medium/<int:id>', methods=["DELETE"])
@media.route('/ireporter/api/v2/red-flags/images/<int:id>', methods=["DELETE"])
@media.route('/ireporter/api/v2/red-flags/videos/<int:id>', methods=["DELETE"])
@media.route('/ireporter/api/v2/red-flags/comments/<int:id>', methods=["DELETE"])
def delete_media(id):

    mediaDB = MediaDB()
    result = mediaDB.delete(id)

    if not result['status']:
        print('***** in post '+str(result['message']))
        return jsonify({"status":400, "error":"Sorry, request not successful try again"}), 400

    return jsonify({"status":200,
                    "data":{"id":id,"message":"Record successfully deleted"}
                    }), 200
