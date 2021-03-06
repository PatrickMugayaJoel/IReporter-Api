import unittest
from app import app
import json
from database.users_db import UsersDB


class TestUsersOne(unittest.TestCase):

    def setUp(self):
        self.test_client = app.test_client()
        self.db = UsersDB()
        self.db.default_users()
    
    def tearDown(self):
        self.test_client.delete
        self.db.delete_default_users()


    def test_user_register_with_no_data(self):

        response  = self.test_client.post(
            'ireporter/api/v2/auth/signup',
            content_type='application/json'
        )

        responsedata = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 400)
        self.assertEqual(responsedata['error'], 'No data posted')

    def test_user_register_with_data(self):

        user = {
                    "firstname":"test3",
                    "lastname":"test3",
                    "username":"test3",
                    "email":"jj@jj.cm",
                    "phonenumber":706084841,
                    "password":"test2"
                }

        response  = self.test_client.post(
            'ireporter/api/v2/auth/signup',
            content_type='application/json',
            data=json.dumps(user)
        )
        responsedata = json.loads(response.data.decode())

        self.assertEqual(response.status_code, 201)
        self.assertEqual(responsedata['data'][0]['user']['firstname'], 'test3')

    def test_existing_user_register(self):

        user = {
                    "firstname":"test2",
                    "lastname":"test2",
                    "username":"test2",
                    "email":"j@jj.cm",
                    "phonenumber":706084841,
                    "password":"test2"
                }

        self.test_client.post(
            'ireporter/api/v2/auth/signup',
            content_type='application/json',
            data=json.dumps(user)
        )

        response  = self.test_client.post(
            'ireporter/api/v2/auth/signup',
            content_type='application/json',
            data=json.dumps(user)
        )
        responsedata = json.loads(response.data.decode())

        self.assertEqual(response.status_code, 400)
        self.assertEqual(responsedata['error'], 'User already exists')

    def test_get_red_flags(self):

        response  = self.test_client.get(
            'ireporter/api/v2/red-flags',
            content_type='application/json'
        )

        self.assertEqual(response.status_code, 404)
        self.assertTrue(b'No red-flags found' in response.data)

    def test_wronguser_register(self):
        user = {
            "firstname":"",
            "lastname":"",
            "username":"",
            "email":"",
            "phonenumber":"",
            "password":""
        }

        response  = self.test_client.post(
            'ireporter/api/v2/auth/signup',
            content_type='application/json',
            data=json.dumps(user)
        )
        responsedata = json.loads(response.data.decode())

        self.assertEqual(response.status_code, 400)
        self.assertTrue('firstname can not be empty' in str(responsedata))


    def test_errorpage(self):

        response  = self.test_client.get('/joel')
        responsedata = json.loads(response.data.decode())

        self.assertEqual(response.status_code, 404)
        self.assertTrue('You have entered an unknown URL.', str(responsedata))

