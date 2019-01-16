import unittest
from app import app
import json
from database.users_db import UsersDB


class TestUsersTwo(unittest.TestCase):

    def setUp(self):
        self.test_client = app.test_client()
        self.user = {
                    "firstname":"test",
                    "lastname":"test",
                    "username":"test",
                    "email":"j@j.cm",
                    "phonenumber":706084841,
                    "password":"test"
                }

        response  = self.test_client.post(
            'ireporter/api/v2/users',
            content_type='application/json',
            data=json.dumps(self.user)
        )
        self.responsedata = json.loads(response.data.decode())

        response = self.test_client.post('/ireporter/api/v2/login', data=json.dumps({"username":"test", "password":"test"}), content_type='application/json')
        data = json.loads(response.data)
        token = data.get('access_token')
        self.headers = {"Content-Type": "application/json", 'Authorization': f'Bearer {token}'}


    
    def tearDown(self):
        db = UsersDB()
        db.delete_user(self.responsedata['data'][0]['id'])
