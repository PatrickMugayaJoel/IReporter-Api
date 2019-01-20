
import json
from flask import jsonify

class Redflag:

    """ Redflag model structure """

    def __init__(self, **kwags):
        
        self.location = kwags.get('location')
        self.description = kwags.get('description')
        self.id = kwags.get('id')
        self.createdon = kwags.get('createdon')
        self.createdby = kwags.get('createdby')
        self.type = kwags.get('type')
        self.title = kwags.get('title')
        self.status = kwags.get('status')
