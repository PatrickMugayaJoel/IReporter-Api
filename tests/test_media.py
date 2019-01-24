import unittest
from app import app
import json
from database.users_db import UsersDB
from database.incidents_db import IncidentsDB


class TestUsersTwo(unittest.TestCase):

    def setUp(self):
        self.test_client = app.test_client()
        self.db = UsersDB()
        self.db.default_users()

        incidents_db = IncidentsDB()
        incidents_db.default_flag()

        response = self.test_client.post('/ireporter/api/v2/auth/login', data=json.dumps({"username":"admin", "password":"admin"}), content_type='application/json')
        data = json.loads(response.data)
        token = data.get('data')[0]['token']
        self.headers = {"Content-Type": "application/json", 'Authorization': f'Bearer {token}'}

    
    def tearDown(self):
        self.test_client.delete
        self.db.delete_default_users()

    def test_add_media(self):

        response  = self.test_client.post(
            'ireporter/api/v2/red-flags/1/images',
            content_type='application/json',
            headers=self.headers,
            data=json.dumps({'type':'image','input':'image'})
        )
        responsedata = json.loads(response.data.decode())

        self.assertEqual(response.status_code, 201)
        self.assertEqual(responsedata['data'][0]['message'], 'image successfully added')

    def test_empty_type_media(self):

        response  = self.test_client.post(
            'ireporter/api/v2/red-flags/1/images',
            content_type='application/json',
            headers=self.headers,
            data=json.dumps({'type':'','input':'image'})
        )
        responsedata = json.loads(response.data.decode())

        self.assertEqual(response.status_code, 400)
        self.assertEqual(responsedata['error'], 'type should be a string')

    def test_wrong_type_media(self):

        response  = self.test_client.post(
            'ireporter/api/v2/red-flags/1/images',
            content_type='application/json',
            headers=self.headers,
            data=json.dumps({'type':'joel','input':'image'})
        )
        responsedata = json.loads(response.data.decode())

        self.assertEqual(response.status_code, 400)
        self.assertEqual(responsedata['error'], 'Valid types are video and image.')

    def test_wrong_input_media(self):

        response  = self.test_client.post(
            'ireporter/api/v2/red-flags/1/images',
            content_type='application/json',
            headers=self.headers,
            data=json.dumps({'type':'image','input':3})
        )
        responsedata = json.loads(response.data.decode())

        self.assertEqual(response.status_code, 400)
        self.assertEqual(responsedata['error'], 'Input should be a string')

    def test_no_flag_post_media(self):

        response  = self.test_client.post(
            'ireporter/api/v2/red-flags/100/images',
            content_type='application/json',
            headers=self.headers,
            data=json.dumps({'type':'image','input':'image'})
        )
        responsedata = json.loads(response.data.decode())

        self.assertEqual(response.status_code, 404)
        self.assertEqual(responsedata['error'], "Redflag with id '100' not found")

    def test_no_flag_get_media(self):

        response  = self.test_client.get(
            'ireporter/api/v2/red-flags/100/images',
            content_type='application/json'
        )
        responsedata = json.loads(response.data.decode())

        self.assertEqual(response.status_code, 404)
        self.assertEqual(responsedata['error'], "Redflag with id '100' not found")

    def test_get_images(self):

        self.test_client.post(
            'ireporter/api/v2/red-flags/1/images',
            content_type='application/json',
            headers=self.headers,
            data=json.dumps({'type':'image','input':'image'})
        )

        response = self.test_client.get(
            'ireporter/api/v2/red-flags/1/images',
            content_type='application/json'
        )
        responsedata = json.loads(response.data.decode())

        self.assertEqual(response.status_code, 200)
        self.assertTrue('image' in str(responsedata))

    def test_get_a_image(self):

        resp = self.test_client.post(
            'ireporter/api/v2/red-flags/1/images',
            content_type='application/json',
            headers=self.headers,
            data=json.dumps({'type':'image','input':'image'})
        )
        resp_data = json.loads(resp.data.decode())

        response = self.test_client.get(
            f'ireporter/api/v2/images/{resp_data["data"][0]["id"]}',
            content_type='application/json'
        )
        responsedata = json.loads(response.data.decode())

        self.assertEqual(response.status_code, 200)
        self.assertTrue('image' in str(responsedata))

    def test_delete_a_image(self):

        resp = self.test_client.post(
            'ireporter/api/v2/red-flags/1/images',
            content_type='application/json',
            headers=self.headers,
            data=json.dumps({'type':'image','input':'image'})
        )
        resp_data = json.loads(resp.data.decode())

        response = self.test_client.delete(
            f'ireporter/api/v2/images/{resp_data["data"][0]["id"]}',
            content_type='application/json',
            headers=self.headers
        )
        responsedata = json.loads(response.data.decode())

        self.assertEqual(response.status_code, 200)
        self.assertTrue('Record successfully deleted' in str(responsedata))

    def test_delete_image_unauthorized(self):

        resp = self.test_client.post(
            'ireporter/api/v2/red-flags/1/images',
            content_type='application/json',
            headers=self.headers,
            data=json.dumps({'type':'image','input':'image'})
        )
        resp_data = json.loads(resp.data.decode())

        response = self.test_client.post('/ireporter/api/v2/auth/login', data=json.dumps({"username":"user", "password":"user"}), content_type='application/json')
        token = json.loads(response.data).get('data')[0]['token']

        response = self.test_client.delete(
            f'ireporter/api/v2/images/{resp_data["data"][0]["id"]}',
            headers={"Content-Type": "application/json", 'Authorization': f'Bearer {token}'}
        )
        responsedata = json.loads(response.data.decode())

        self.assertEqual(response.status_code, 401)
        self.assertTrue('Sorry! you are not authorised to perform this action.' in str(responsedata))

    def test_delete_missing_image(self):

        response = self.test_client.delete(
            f'ireporter/api/v2/images/0',
            headers=self.headers
        )
        responsedata = json.loads(response.data.decode())

        self.assertEqual(response.status_code, 404)
        self.assertTrue('Item not found' in str(responsedata))

    def test_missing_media(self):

        response = self.test_client.get(
            'ireporter/api/v2/red-flags/1/videos',
            content_type='application/json'
        )
        responsedata = json.loads(response.data.decode())

        self.assertEqual(response.status_code, 200)
        self.assertTrue('No data to display.' in str(responsedata))

    def test_missing_image(self):

        response = self.test_client.get(
            'ireporter/api/v2/images/0',
            content_type='application/json'
        )
        responsedata = json.loads(response.data.decode())

        self.assertEqual(response.status_code, 200)
        self.assertTrue('Sorry, resource not found.' in str(responsedata))
