
import unittest
from app import app
import json
from database.users_db import UsersDB
from database.redflags_db import RedflagsDB

class TestMainNoData(unittest.TestCase):

    def setUp(self):
        self.test_client = app.test_client()
        self.db = UsersDB()
        self.db.default_users()
        self.red_flag = {
                    "title":"trest",
                    "type":"redflag",
                    "location":"7888876, 5667788",
                    "comment":""
                    }

        response = self.test_client.post('/ireporter/api/v2/auth/login', data=json.dumps({"username":"admin", "password":"admin"}), content_type='application/json')
        self.data = json.loads(response.data)
        token = self.data.get('data')[0]['token']
        self.headers = {"Content-Type": "application/json", 'Authorization': f'Bearer {token}'}


    def tearDown(self):
        self.test_client.delete
        self.db.delete_default_users()



    def test_create_wrong_red_flag(self):

        response  = self.test_client.post(
            'ireporter/api/v2/red-flags',
            content_type='application/json',
            headers=self.headers,
            data=json.dumps(self.red_flag)
        )

        self.assertEqual(response.status_code, 400)
        self.assertTrue(b'comment can not be empty' in response.data)

    def test_create_empty_red_flag(self):

        response  = self.test_client.post(
            'ireporter/api/v2/red-flags',
            headers=self.headers,
            content_type='application/json'
        )

        self.assertEqual(response.status_code, 400)
        self.assertTrue(b'No data was posted' in response.data)

    def test_get_red_flag(self):

        response  = self.test_client.get(
            'ireporter/api/v2/red-flags/1',
            headers=self.headers,
            content_type='application/json'
        )

        self.assertEqual(response.status_code, 404)
        self.assertTrue(b'red-flag not found' in response.data)

    def test_delete_red_flag(self):

        response  = self.test_client.delete(
            'ireporter/api/v2/red-flags/1',
            headers=self.headers,
            content_type='application/json'
        )

        self.assertEqual(response.status_code, 404)
        self.assertTrue(b'red-flag not found' in response.data)

    def test_put_red_flag_wrong2(self):

        response  = self.test_client.patch(
            'ireporter/api/v2/red-flags/1/comment',
            content_type='application/json',
            headers=self.headers,
            data=json.dumps(self.red_flag)
        )

        self.assertEqual(response.status_code, 404)
        self.assertTrue(b'red-flag not found' in response.data)

    def test_create_empty_media(self):

        response  = self.test_client.post(
            'ireporter/api/v2/red-flags/1/images',
            content_type='application/json'
        )

        self.assertEqual(response.status_code, 400)
        self.assertTrue(b'No data posted' in response.data)

    def test_request_method_error(self):

        response  = self.test_client.patch(
            'ireporter/api/v2/images/1',
            content_type='application/json'
        )

        self.assertEqual(response.status_code, 405)
        self.assertTrue(b'Request method error.' in response.data)
