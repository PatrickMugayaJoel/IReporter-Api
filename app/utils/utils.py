
import time
import jwt
from datetime import timedelta, datetime
from database.incidents_db import IncidentsDB


def serialize(objt):

    """ Method receives an object and returns a dictionary """

    if isinstance(objt, list):
        listtwo = []
        for item in objt:
            listtwo.append(serialize(item))
        return listtwo
    else: return objt.__dict__

def get_flag_by_id(id):

    """ get flag by id """

    incidents_db = IncidentsDB()
    regflag = incidents_db.check_flag(id)

    if regflag and regflag != 'False':
        return regflag
    else:
        regflag = None
        return regflag

def encode_handler(identity, JWT_SECRET_KEY, JWT_ALGORITHM):

    """ method generates a jwt token """

    payload = payload_handler(identity)
    return jwt.encode(payload, JWT_SECRET_KEY, algorithm=JWT_ALGORITHM, headers=None)

def payload_handler(identity):

    """ method builds playload that will be added to the JWT token  """

    iat = datetime.utcnow()
    exp = iat + timedelta(hours=20)
    nbf = iat + timedelta(seconds=0)
    identity = getattr(identity, 'id') or identity['id']
    return {'exp': exp, 'iat': iat, 'nbf': nbf, 'identity': identity}
