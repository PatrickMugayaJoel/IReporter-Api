
from flask import jsonify, request, Blueprint, flash, redirect
from flask_jwt_extended import jwt_required, get_jwt_identity
from database.media_db import MediaDB
from app.utils.utils import get_flag_by_id
from werkzeug.utils import secure_filename
import os

UPLOAD_FOLDER = '../uploads'
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])

media = Blueprint('media_view', __name__)

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@media.route('/ireporter/api/v2/red-flags/<int:id>/images', methods=["POST"])
@media.route('/ireporter/api/v2/red-flags/<int:id>/videos', methods=["POST"])
def upload_file(id):
    if request.method == 'POST':

        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']

        # submit a empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        print(file.filename)
        if file and allowed_file(file.filename):
            filename = 'uploads/'+secure_filename(file.filename)
            file.save(""+filename)
            return filename,200
    return "success",200

""" def postmedia(id):

    try:
        f = request.files['file']
    except:
        return jsonify({"status":400, "error":"No data posted"}), 400

    # if not (data.get('type') and isinstance(data.get('type'), str) and (not data['type'].isspace())):
        # return jsonify({"status":400, "error":"type should be a string"}), 400

    # if not (data['type'] in ["image","video"]):
        # return jsonify({"status":400, "error":"Valid types are video and image."}), 400

    # if not (data.get('input') and isinstance(data.get('input'), str) and (not data['input'].isspace())):
        # return jsonify({"status":400, "error":"Input should be a string"}), 400

    if not get_flag_by_id(id):
        return jsonify({"status":404, "error":f"Redflag with id '{id}' not found"}), 404

    saveresult = f.save(secure_filename(f.filename))
    print('Saving: '+str(saveresult))
    print('f: '+str(f))
    formdata = request.form
    data ={'type':formdata.get('type'),'input':f.filename, 'redflag': formdata.get('id')}

    # mediaDB = MediaDB() [('mytype', 'image'), ('id', '1')]
    # result = mediaDB.add(**data)

    # return jsonify({"status":201,
    #                 "data":[{
    #                     "id":result['data']['id'],
    #                     "message":f"{data['type']} successfully added",
    #                 }]}), 201
    return jsonify(str(data)), 200 """


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
