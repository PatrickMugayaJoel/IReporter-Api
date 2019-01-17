
from flask import jsonify
from app import app

@app.errorhandler(404)
def page_not_found(e):
    valid_urls = {
        'Welcome': {
            'url': '/',
            'method(s)': 'GET'
            },
        'Signup': {
            'url': '/ireporter/api/v2/users',
            'method(s)': 'POST',
            'POST':[
                        {
                            'body': {
                            "firstname*":"string",
                            "lastname*":"string",
                            "othernames":"string",
                            "username*":"string",
                            "email*":"example@email.com",
                            "phonenumber*":"phone no",
                            "password*":"Atleast 8 characters"
                            }
                        }
                    ]
            },
        'Redflags': {
            'url': '/ireporter/api/v2/red-flags',
            'method(s)': 'GET, POST',
            'GET':'Takes no body',
            'POST':'Body is as defined below. "key*" means required.',
            'body': {
                "title*":"string",
                "type*":"string",
                "description*":"string",
                "location*":"string",
                "comment":"string",
                "Videos":"link",
                "Images":"link"
                }
            },
        'Redflag': {
            'url': '/ireporter/api/v2/red-flags/<int:id>',
            'method(s)': 'GET, DELETE, PUT',
            'GET & DELETE':'Take no body',
            'PUT':'All fields in the body are optional but atleast one should have data',
            'body': {
                "title":"string",
                "type":"string",
                "description":"string",
                "location":"string",
                "comment":"string",
                "Videos":"link",
                "Images":"link"
                }
            }
    }
    return jsonify ({
        'Error': 'You have entered an unknown URL.',
        'Valid URLs': valid_urls,
        'message': 'Please contact JoseanPatrick for details about this API.'
        }), 404

@app.errorhandler(500)
def server_error(e):
    return jsonify ({
        'Error': 'Server error. We apologise for the inconvenience.',
        'message': 'Please try again or report the issue to the auther. Thank you.'
        }), 400

@app.errorhandler(405)
def request_method_error(e):
    return jsonify ({
        'Error': 'Request method error.',
        'message': 'You are trying to access a resource with a wrong request method.'
        }), 405
