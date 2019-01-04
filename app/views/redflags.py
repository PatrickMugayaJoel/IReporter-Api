
import datetime
from flask import jsonify, request
from app import app
from app.utils.utils import serialize, generate_id
from app.utils.validate_redflag import Validate_redflag
from app.models.redflag import Redflag

regflags = list()

@app.route('/ireporter/api/v2/red-flags', methods=["GET"])
def getredflags():

    """ get red-flags """
    if request.method == 'GET':

        if regflags:
            allredflags = serialize(regflags)
            return jsonify({"status":200,
                            "data":allredflags
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
    
    try:
        title = next((item for item in regflags if item.title == new_red_flag.title))
    except: title = None
    
    if title:
        return jsonify({"status":400, "error":"Incident already exists"}), 400
    
    new_red_flag.id = generate_id()
    new_red_flag.createdOn = datetime.datetime.now().strftime("%Y/%m/%d")
    new_red_flag.createdBy = 1
    new_red_flag.status = 'under investigation'

    validate_redflag = Validate_redflag()
    thisredflag = validate_redflag.validate(**serialize(new_red_flag))

    if thisredflag['message'] != 'successfully validated':
        return jsonify({"status":400,
                        "error":thisredflag['message']}), 400

    regflags.append(new_red_flag)

    return jsonify({"status":201,
                    "data":[{
                        "id":new_red_flag.id,
                        "message":"Created red-flag Record"
                        }]
                    }), 201



def get_flag_by_id(id):
    """ get flag by id """

    if regflags:
        try:
            regflag = next((item for item in regflags if item.id == id))
            return regflag
        except:
            regflag = None
            return regflag
    else:
        regflag = None
        return regflag

@app.route('/ireporter/api/v2/red-flags/<int:id>', methods=["GET"])
def get(id):

    regflag = get_flag_by_id(id)
    
    if regflag:
        return jsonify({"status":200,
                        "data":serialize(regflag)
                        }), 200

    return jsonify({"status":404, "error":"Redflag not found"}), 404

@app.route('/ireporter/api/v2/red-flags/<int:id>', methods=["DELETE"])
def delete(id):

    regflag = get_flag_by_id(id)

    if regflag:
        regflags.remove(regflag)
        return jsonify({"status":200,
                        "message":"Deleted red-flag Record"
                        }), 200

    return jsonify({"status":404, "error":"Redflag not found"}), 404

@app.route('/ireporter/api/v2/red-flags/<int:id>', methods=["PUT"])
def put(id):

    regflag = get_flag_by_id(id)
        
    try: data = request.get_json()
    except: return jsonify({"status":400, "error":"No data was posted"}), 400

    if not regflag:
        return jsonify({"status":404, "error":"Redflag not found"}), 404

    flag = serialize(Redflag(**serialize(regflag)))
    
    for key in data:
        flag[key] = data[key]

    validate_redflag = Validate_redflag()
    validity = validate_redflag.validate(**flag)

    if validity['message'] == 'successfully validated':
        regflag.add(**flag)

        return jsonify({"status":200,
                        "message":"Updated red-flag Record"
                        }), 200
    else:
        return jsonify({"status":400, "error":validity['message']}), 400

@app.route('/clearflags')
def clearflags():
    """ clear out data """
    del regflags[:]
    return 'True', 200
