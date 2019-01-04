
import json
from flask import jsonify

class Redflag:

    """ Redflag model structure """

    def __init__(self, **kwags):

        self.Images = list()
        self.Videos = list()
        self.comment = list()

        if kwags.get('Images'):
            self.Images.append(kwags.get('Images'))
        if kwags.get('Videos'):
            self.Videos.append(kwags.get('Videos'))
        if kwags.get('comment'):
            self.comment.append(kwags.get('comment'))
        
        self.location = kwags.get('location')
        self.description = kwags.get('description')
        self.id = kwags.get('id')
        self.createdOn = kwags.get('createdOn')
        self.createdBy = kwags.get('createdBy')
        self.type = kwags.get('type')
        self.title = kwags.get('title')
        self.status = kwags.get('status')

    def add(self, **kwags):
        
        if kwags.get('Images') != self.Images:
            self.Images.append(kwags.get('Images'))
        if kwags.get('Videos') != self.Videos:
            self.Videos.append(kwags.get('Videos'))
        if kwags.get('comment') != self.comment:
            self.comment.append(kwags.get('comment'))
        
        self.location = kwags.get('location')
        self.description = kwags.get('description')
        self.id = kwags.get('id')
        self.createdOn = kwags.get('createdOn')
        self.createdBy = kwags.get('createdBy')
        self.type = kwags.get('type')
        self.title = kwags.get('title')
        self.status = kwags.get('status')
