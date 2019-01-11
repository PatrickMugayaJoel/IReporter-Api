
from datetime import timedelta, datetime
from flask import jsonify
from flask import Flask
from flask_jwt import JWT, jwt_required, current_identity
from app.models.user import User
from database.users_db import UsersDB
from app.views.users import users_view


db = UsersDB()
app = Flask(__name__)

app.config['JWT_SECRET_KEY'] = 'joel@Da4!'
app.config['JWT_AUTH_URL_RULE'] = '/ireporter/api/v2/login'
app.config['JWT_AUTH_HEADER_PREFIX'] = 'Bearer'
app.config['JWT_EXPIRATION_DELTA'] = timedelta(hours=10)

def authenticate(username, password):
    users = db.login(username, password)
    if users and users != 'False':
            user=User(**users)
            user.id = users['userid']
            app.config['JWT_SECRET_KEY'] = str(users['userid'])+str(datetime.now())
            return user

def identity(payload):
    user = db.check_id(payload['identity'])
    if user and user != 'False':
            return user

jwt = JWT(app, authenticate, identity)


app.register_blueprint(users_view)

from app.views import redflags, error_handlers

#index route
@app.route('/')
def home():
    """ home route """
    
    return jsonify({"status":200,
                            "data":[{
                                "message":"Welcome"
                            }]}), 200


@jwt.auth_response_handler
def customized_response_handler(access_token, identity):
    return jsonify({
                        'access_token': access_token.decode('utf-8'),
                        'status': 200
                   })

@jwt.jwt_error_handler
def customized_error_handler(error):
    return jsonify({
                       'error': error.description,
                       'status': error.status_code
                   }), error.status_code

@app.route('/ireporter/api/v2/logout')
@jwt_required()
def logout():

    app.config['JWT_SECRET_KEY'] = str(current_identity['userid'])+str(datetime.now())

    return jsonify ({
        'message': 'successfully logged out'
    }), 200  
