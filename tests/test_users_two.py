import unittest
from app import app
import json
from database.users_db import UsersDB


class TestUsersTwo(unittest.TestCase):

    def setUp(self):
        self.test_client = app.test_client()
        self.db = UsersDB()
        self.db.default_users()

        response = self.test_client.post('/ireporter/api/v2/auth/login', data=json.dumps({"username":"admin", "password":"admin"}), content_type='application/json')
        data = json.loads(response.data)
        token = data['data'][0].get('token')
        self.headers = {"Content-Type": "application/json", 'Authorization': f'Bearer {token}'}

    
    def tearDown(self):
        self.test_client.delete
        self.db.delete_default_users()

    def test_get_users(self):

        response  = self.test_client.get(
            'ireporter/api/v2/users',
            headers=self.headers
        )
        responsedata = json.loads(response.data.decode())

        self.assertEqual(response.status_code, 200)
        self.assertTrue('phonenumber' in str(responsedata))

    def test_get_users_unauthorized(self):

        response = self.test_client.post('/ireporter/api/v2/auth/login', data=json.dumps({"username":"user", "password":"user"}), content_type='application/json')
        token = json.loads(response.data).get('data')[0]['token']

        response  = self.test_client.get(
            'ireporter/api/v2/users',
            headers={"Content-Type": "application/json", 'Authorization': f'Bearer {token}'}
        )
        responsedata = json.loads(response.data.decode())

        self.assertEqual(response.status_code, 401)
        self.assertTrue('Sorry! Access restricted to administrators.' in str(responsedata))

    def test_get_a_user(self):

        response  = self.test_client.get(
            'ireporter/api/v2/users/10',
            headers=self.headers
        )
        responsedata = json.loads(response.data.decode())

        self.assertEqual(response.status_code, 200)
        self.assertTrue('phonenumber' in str(responsedata))

    def test_get_a_user_unauthorized(self):

        response = self.test_client.post('/ireporter/api/v2/auth/login', data=json.dumps({"username":"user", "password":"user"}), content_type='application/json')
        token = json.loads(response.data).get('data')[0]['token']

        response  = self.test_client.get(
            'ireporter/api/v2/users/10',
            headers={"Content-Type": "application/json", 'Authorization': f'Bearer {token}'}
        )
        responsedata = json.loads(response.data.decode())

        self.assertEqual(response.status_code, 401)
        self.assertTrue('Sorry! Access denied.' in str(responsedata))

    def test_get_a_missing_user(self):

        response  = self.test_client.get(
            'ireporter/api/v2/users/0',
            headers=self.headers
        )
        responsedata = json.loads(response.data.decode())

        self.assertEqual(response.status_code, 404)
        self.assertTrue('User not found' in str(responsedata))

    def test_user_update(self):

        user = {
                    "firstname":"joel",
                    "lastname":"joel",
                    "username":"joel",
                    "email":"pj@jj.cm",
                    "phonenumber":706084841,
                    "password":"joel"
                }

        response = self.test_client.put(
            f'ireporter/api/v2/users/20',
            headers=self.headers,
            data=json.dumps(user)
        )
        responsedata = json.loads(response.data.decode())

        self.assertEqual(response.status_code, 200)
        self.assertTrue('Updated User record' in str(responsedata))

    def test_user_update_no_data(self):

        response = self.test_client.put(
            f'ireporter/api/v2/users/20',
            headers=self.headers
        )
        responsedata = json.loads(response.data.decode())

        self.assertEqual(response.status_code, 400)
        self.assertTrue('No data posted' in str(responsedata))

    def test_user_update_unauthorized(self):

        user = {
                    "firstname":"joel",
                    "lastname":"joel",
                    "username":"joel",
                    "email":"pj@jj.cm",
                    "phonenumber":706084841,
                    "password":"joel"
                }

        response = self.test_client.post('/ireporter/api/v2/auth/login', data=json.dumps({"username":"user", "password":"user"}), content_type='application/json')
        token = json.loads(response.data).get('data')[0]['token']

        response = self.test_client.put(
            f'ireporter/api/v2/users/10',
            headers={"Content-Type": "application/json", 'Authorization': f'Bearer {token}'},
            data=json.dumps(user)
        )
        responsedata = json.loads(response.data.decode())

        self.assertEqual(response.status_code, 401)
        self.assertTrue('Sorry! Access denied.' in str(responsedata))

    def test_absent_user_update(self):

        user = {
                    "firstname":"joel",
                    "lastname":"joel",
                    "username":"joel",
                    "email":"pj@jj.cm",
                    "phonenumber":706084841,
                    "password":"joel"
                }

        response = self.test_client.put(
            f'ireporter/api/v2/users/0',
            headers=self.headers,
            data=json.dumps(user)
        )
        responsedata = json.loads(response.data.decode())

        self.assertEqual(response.status_code, 404)
        self.assertTrue('User not found' in str(responsedata))

    def test_existing_user_update(self):

        user = {
                    "firstname":"admin",
                    "lastname":"admin",
                    "username":"admin",
                    "email":"j@jj.cm",
                    "phonenumber":706084841,
                    "password":"admin"
                }

        response = self.test_client.put(
            f'ireporter/api/v2/users/20',
            headers=self.headers,
            data=json.dumps(user)
        )
        responsedata = json.loads(response.data.decode())

        self.assertEqual(response.status_code, 400)
        self.assertTrue('User update failed' in str(responsedata))

    def test_wrong_user_update(self):

        user = {
                    "firstname":"joel",
                    "lastname":"joel",
                    "username":" ",
                    "phonenumber":706084841,
                    "password":"joel"
                }

        response = self.test_client.put(
            f'ireporter/api/v2/users/20',
            headers=self.headers,
            data=json.dumps(user)
        )
        responsedata = json.loads(response.data.decode())

        self.assertEqual(response.status_code, 400)
        self.assertTrue('username must be a string.' in str(responsedata))
