
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
    else:
        return objt.__dict__


def get_flag_by_id(id):
    """ get flag by id """

    incidents_db = IncidentsDB()
    regflag = incidents_db.check_flag(id)

    if regflag and regflag != 'False':
        return regflag
    else:
        regflag = None
        return regflag
