
import os
from werkzeug.utils import secure_filename
from flask import jsonify, request, Blueprint, send_file
from flask_jwt_extended import jwt_required, get_jwt_identity
from database.media_db import MediaDB
from app.utils.utils import get_flag_by_id


UPLOAD_FOLDER = '../uploads'
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])

media = Blueprint('media_view', __name__)

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@media.route('/ireporter/api/v2/red-flags/<int:id>/images', methods=["POST"])
@media.route('/ireporter/api/v2/red-flags/<int:id>/videos', methods=["POST"])
def upload_file(id):

    # check if the post request has the file part
    if 'file' not in request.files:
        return jsonify({'error':'No file part'}), 400
    file = request.files['file']

    if not get_flag_by_id(id):
        return jsonify({"status":404, "error":f"Redflag with id '{id}' not found"}), 404

    # submit a empty part without filename
    if file.filename == '':
        return jsonify({'error':'No selected file'}), 400

    if file and allowed_file(file.filename):
        filename = 'uploads/'+secure_filename(file.filename)

        try:
            file.save(filename)
        except Exception as exc:
            return str(exc), 400

        formdata = request.form

        if not (formdata.get('type') in ["image","video"]):
            return jsonify({"status":400, "error":"Valid types are video and image."}), 400

        data ={'type':formdata.get('type'),'input':file.filename, 'redflag': formdata.get('id')}

        mediaDB = MediaDB()
        result = mediaDB.add(**data)

        return jsonify({"status":201,
                        "data":[{
                            "id":result['data']['id'],
                            "message":f"{data['type']} successfully added",
                        }]}), 201

def root_dir():
    return os.path.abspath(os.path.dirname(__file__))

@media.route('/ireporter/api/v2/files/images/<filename>')
def get_file(filename):
    try:
        # src = os.path.join(root_dir(), '../../uploads/'+filename)
        return send_file('uploads/'+filename), 200
    except IOError as exc:
        return str(exc)


@media.route('/ireporter/api/v2/red-flags/<int:id>/<type>', methods=["GET"])
def getmedia(type, id):

    """ funtion to return a list of media """

    type = type.rstrip('s')

    if not get_flag_by_id(id):
        return jsonify({"status":404, "error":f"Redflag with id '{id}' not found"}), 404

    mediaDB = MediaDB()
    result = mediaDB.flag_media(**{'type':type,'redflag':id})
    
    if not result['data']:
        return jsonify({"status":200, "message":"No data to display."})
    
    images = [item[0] for item in result['data'] ]
    
    return jsonify({"status":200,
                    "data":images
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
@jwt_required
def delete_media(id):

    """ function to delete a video/image """

    mediaDB = MediaDB()
    medium = mediaDB.check_id(id)

    medium = medium.get('data')

    if not medium:
        return jsonify({"status":404, "error":"Item not found"}), 404

    regflag = get_flag_by_id(medium.get('redflag'))

    if not (get_jwt_identity()['is_admin'] or (get_jwt_identity()['userid'] == regflag['createdby']) ):
        return jsonify({"status":401,
                        "data":[{
                            "message":"Sorry! you are not authorised to perform this action.",
                        }]}), 401

    mediaDB.delete(id)

    return jsonify({"status":200,
                    "data":{"id":id,"message":"Record successfully deleted"}
                    }), 200
