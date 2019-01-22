
import time
import jwt
from datetime import timedelta, datetime
from database.redflags_db import RedflagsDB


def serialize(objt):
    if isinstance(objt, list):
        listtwo = []
        for item in objt:
            listtwo.append(serialize(item))
        return listtwo
    else: return objt.__dict__
 
def generate_id():
   now = time.time()
   localtime = time.localtime(now)
   milliseconds = '%03d' % int((now - int(now)) * 1000)
   return int(time.strftime('%Y%m%d%H%M%S', localtime) + milliseconds)

def get_flag_by_id(id):
    """ get flag by id """

    regflagdb = RedflagsDB()
    regflag = regflagdb.check_flag(id)

    if regflag and regflag != 'False':
        return regflag
    else:
        regflag = None
        return regflag

def encode_handler(identity, JWT_SECRET_KEY, JWT_ALGORITHM):
    payload = payload_handler(identity)
    return jwt.encode(payload, JWT_SECRET_KEY, algorithm=JWT_ALGORITHM, headers=None)

def payload_handler(identity):
    iat = datetime.utcnow()
    exp = iat + timedelta(hours=10)
    nbf = iat + timedelta(seconds=0)
    identity = getattr(identity, 'id') or identity['id']
    return {'exp': exp, 'iat': iat, 'nbf': nbf, 'identity': identity}
