import unittest
from app import app
import json
from database.users_db import UsersDB
from database.redflags_db import RedflagsDB

class TestMain(unittest.TestCase):

    def setUp(self):
        self.test_client = app.test_client()
        #self.flags_db = RedflagsDB()
        self.db = UsersDB()
        self.db.default_users()
        self.red_flag = {
                    "title":"trest",
                    "type":"redflag",
                    "location":"7888876, 5667788",
                    "description":"description",
                    "comment":"comment"
                    }

        response = self.test_client.post('/ireporter/api/v2/login', data=json.dumps({"username":"admin", "password":"admin"}), content_type='application/json')
        self.data = json.loads(response.data)
        token = self.data.get('access_token')
        self.headers = {"Content-Type": "application/json", 'Authorization': f'Bearer {token}'}


    def tearDown(self):
        self.test_client.delete
        self.db.delete_default_users()



    def test_home(self):

        response  = self.test_client.get('/')
        responsedata = json.loads(response.data.decode())

        self.assertEqual(response.status_code, 200)
        self.assertTrue('welcome', str(responsedata))

    def test_create_red_flag(self):

        response  = self.test_client.post(
            'ireporter/api/v2/red-flags',
            content_type='application/json',
            headers=self.headers,
            data=json.dumps(self.red_flag)
        )
        responsedata = json.loads(response.data.decode())

        self.assertEqual(response.status_code, 201)
        self.assertEqual(responsedata['data'][0]['message'], 'Created red-flag Record')

    def test_create_red_flag_wrong_type(self):

        self.red_flag = {
                    "title":"trest",
                    "type":"joel",
                    "location":"7888876, 5667788",
                    "description":"description",
                    "comment":"comment"
                    }

        response  = self.test_client.post(
            'ireporter/api/v2/red-flags',
            content_type='application/json',
            headers=self.headers,
            data=json.dumps(self.red_flag)
        )
        responsedata = json.loads(response.data.decode())

        self.assertEqual(response.status_code, 400)
        self.assertEqual(responsedata['error'], 'Valid types are redflag and intervention.')

    def test_get_red_flags(self):

        self.test_client.post(
            'ireporter/api/v2/red-flags',
            content_type='application/json',
            headers=self.headers,
            data=json.dumps(self.red_flag)
        )

        response = self.test_client.get(
            'ireporter/api/v2/red-flags',
            content_type='application/json'
        )
        responsedata = json.loads(response.data.decode())

        self.assertEqual(response.status_code, 200)
        self.assertTrue('description' in str(responsedata))

    def test_post_duplicate_red_flags(self):

        self.test_client.post(
            'ireporter/api/v2/red-flags',
            content_type='application/json',
            headers=self.headers,
            data=json.dumps(self.red_flag)
        )

        response = self.test_client.post(
            'ireporter/api/v2/red-flags',
            content_type='application/json',
            headers=self.headers,
            data=json.dumps(self.red_flag)
        )
        responsedata = json.loads(response.data.decode())

        self.assertEqual(response.status_code, 400)
        self.assertTrue('Incident already exists' in str(responsedata))

    def test_get_red_flag(self):

        response = self.test_client.post(
            'ireporter/api/v2/red-flags',
            content_type='application/json',
            headers=self.headers,
            data=json.dumps(self.red_flag)
        )
        respdata = json.loads(response.data.decode())

        response  = self.test_client.get(
            f'ireporter/api/v2/red-flags/{respdata["data"][0]["id"]}',
            content_type='application/json'
        )
        responsedata = json.loads(response.data.decode())

        self.assertEqual(response.status_code, 200)
        self.assertEqual(respdata["data"][0]["id"], responsedata["data"]['flag_id'])

    def test_delete_red_flag(self):

        response = self.test_client.post(
            'ireporter/api/v2/red-flags',
            content_type='application/json',
            headers=self.headers,
            data=json.dumps(self.red_flag)
        )
        respdata = json.loads(response.data.decode())

        response = self.test_client.delete(
            f"ireporter/api/v2/red-flags/{respdata['data'][0]['id']}",
            headers=self.headers,
            content_type='application/json'
        )
        responsedata = json.loads(response.data.decode())

        self.assertEqual(response.status_code, 200)
        self.assertEqual(responsedata["message"], 'Deleted red-flag Record')

    def test_delete_red_flag_unauthorized(self):

        response = self.test_client.post(
            'ireporter/api/v2/red-flags',
            content_type='application/json',
            headers=self.headers,
            data=json.dumps(self.red_flag)
        )
        respdata = json.loads(response.data.decode())

        response = self.test_client.post('/ireporter/api/v2/login', data=json.dumps({"username":"user", "password":"user"}), content_type='application/json')
        token = json.loads(response.data).get('access_token')

        response = self.test_client.delete(
            f"ireporter/api/v2/red-flags/{respdata['data'][0]['id']}",
            headers={"Content-Type": "application/json", 'Authorization': f'Bearer {token}'}
        )
        responsedata = json.loads(response.data.decode())

        self.assertEqual(response.status_code, 401)
        self.assertEqual(responsedata["error"], 'Sorry! you are not authorised to perform this action.')

    def test_put_redflag(self):

        response = self.test_client.post(
            'ireporter/api/v2/red-flags',
            content_type='application/json',
            headers=self.headers,
            data=json.dumps(self.red_flag)
        )
        respdata = json.loads(response.data.decode())

        red_flag2 = {
                    "title":"This is it",
                    "location":"123345, 98765",
                    "description":"desc"
                    }

        response  = self.test_client.put(
            f'ireporter/api/v2/red-flags/{respdata["data"][0]["id"]}',
            content_type='application/json',
            headers=self.headers,
            data=json.dumps(red_flag2)
        )
        respdata2 = json.loads(response.data.decode())

        self.assertEqual(respdata2['status'], 200)
        self.assertEqual(respdata2['message'], 'Updated red-flag Record')

    def test_put_redflag_no_data(self):

        response  = self.test_client.put(
            f'ireporter/api/v2/red-flags/0',
            content_type='application/json',
            headers=self.headers
        )
        respdata = json.loads(response.data.decode())

        self.assertEqual(respdata['status'], 400)
        self.assertEqual(respdata['error'], 'No data was posted')

    def test_put_redflag_unauthorized(self):

        response = self.test_client.post(
            'ireporter/api/v2/red-flags',
            content_type='application/json',
            headers=self.headers,
            data=json.dumps(self.red_flag)
        )
        respdata = json.loads(response.data.decode())

        red_flag2 = {
                    "title":"This is it",
                    "location":"123345, 98765",
                    "description":"desc"
                    }

        response = self.test_client.post('/ireporter/api/v2/login', data=json.dumps({"username":"user", "password":"user"}), content_type='application/json')
        token = json.loads(response.data).get('access_token')

        response  = self.test_client.put(
            f'ireporter/api/v2/red-flags/{respdata["data"][0]["id"]}',
            headers={"Content-Type": "application/json", 'Authorization': f'Bearer {token}'},
            data=json.dumps(red_flag2)
        )
        respdata2 = json.loads(response.data.decode())

        self.assertEqual(respdata2['status'], 401)
        self.assertEqual(respdata2['error'], 'Sorry! you are not authorised to perform this action.')

    def test_put_red_flag_wrong(self):

        response = self.test_client.post(
            'ireporter/api/v2/red-flags',
            content_type='application/json',
            headers=self.headers,
            data=json.dumps(self.red_flag)
        )
        resp = json.loads(response.data.decode())

        red_flag2 = {
                    "title":"Redflag",
                    "location":"",
                    "description":"description",
                    "comment":"comment"
                    }

        response  = self.test_client.put(
            f'ireporter/api/v2/red-flags/{resp["data"][0]["id"]}',
            content_type='application/json',
            headers=self.headers,
            data=json.dumps(red_flag2)
        )
        respdata = json.loads(response.data.decode())

        self.assertEqual(response.status_code, 400)
        self.assertTrue('location can not be empty.' in str(respdata['error']))
