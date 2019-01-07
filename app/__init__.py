
from flask import jsonify
from flask import Flask

app = Flask(__name__)

from app.views import redflags, users, error_handlers

#index route
@app.route('/')
def home():
    """ home route """
    
    return jsonify({"status":200,
                            "data":[{
                                "message":"Welcome"
                            }]}), 200