
import json
from flask import jsonify

class Redflag:

    """
    Redflag model class
    """

    def __init__(self, **kwags):
            
        """
        Initialising Redflag model
        """

        self.id = kwags.get('id')
        self.createdon = kwags.get('createdon')
        self.createdby = kwags.get('createdby')
        self.type = kwags.get('type')
        self.location = kwags.get('location')
        self.status = kwags.get('status')
        self.comment = kwags.get('comment')
        self.title = kwags.get('title')
