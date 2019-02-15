
from datetime import timedelta, datetime
from flask import jsonify, request
from flask import Flask
from flasgger import Swagger
from flask_jwt_extended import ( JWTManager, jwt_required, create_access_token, get_jwt_identity, get_raw_jwt)
import json
from app.models.user import User
from database.users_db import UsersDB
from app.views.users import users_view
from app.views.redflags import redflags_view
from app.views.media import media
from app.docs.template import doc_temp
from flask_cors import CORS


db = UsersDB()
app = Flask(__name__)
CORS(app)

swagger = Swagger(app, template=doc_temp)

blacklist = []

app.config['JWT_SECRET_KEY'] = 'joel@Da4!'
app.config['JWT_BLACKLIST_ENABLED'] = True
app.config['JWT_BLACKLIST_TOKEN_CHECKS'] = ['access']

jwt = JWTManager(app)

from app.views import error_handlers

app.register_blueprint(users_view)
app.register_blueprint(redflags_view)
app.register_blueprint(media)

#index route
@app.route('/')
def home():
    """ Index route """
    
    return jsonify({"status":200,
                            "data":[{
                                "message":"Welcome to IReporter 3"
                            }]}), 200

#login route
@app.route('/ireporter/api/v2/auth/login', methods=["POST"])
def login():
    """login"""
    if not request.is_json:
        return jsonify({"message":"Missing JSON data","status":"failed"}), 400

    username = request.json.get('username')
    password = request.json.get('password')

    user = db.login(username, password)
    
    if user and user != 'False':
        userr=User(**user)
        userr.id = user['userid']
        userr.isAdmin = user['is_admin']
        return jsonify({
                            'status': 200, 
                            'data' : [{
                                'token' : create_access_token(identity={'userid':userr.id,'is_admin':userr.isAdmin}, expires_delta=False),
                                'user': userr.__dict__
                            }]
                    }), 200  
    else:
        return jsonify({"error": "Wrong username or password","status":401}), 401

@app.route('/ireporter/api/v2/auth/logout')
@jwt_required
def logout():

    """ function to log a user out """

    jti = get_raw_jwt()['jti']
    blacklist.append(jti)

    return jsonify ({
        'message': 'successfully logged out'
    }), 200  

@jwt.token_in_blacklist_loader
def check_if_token_in_blacklist(decrypted_token):
    
    if decrypted_token['jti'] in blacklist:
        return True
    return decrypted_token == 'true'
