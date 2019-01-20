import unittest
from app import app
import json
from database.users_db import UsersDB
from database.redflags_db import RedflagsDB


class TestUsersTwo(unittest.TestCase):

    def setUp(self):
        self.test_client = app.test_client()
        self.db = UsersDB()
        self.db.default_users()

        flags_db = RedflagsDB()
        flags_db.default_flag()

        response = self.test_client.post('/ireporter/api/v2/login', data=json.dumps({"username":"admin", "password":"admin"}), content_type='application/json')
        data = json.loads(response.data)
        token = data.get('access_token')
        self.headers = {"Content-Type": "application/json", 'Authorization': f'Bearer {token}'}

    
    def tearDown(self):
        self.test_client.delete
        self.db.delete_default_users()

    def test_add_media(self):

        response  = self.test_client.post(
            'ireporter/api/v2/red-flags/10/comments',
            content_type='application/json',
            headers=self.headers,
            data=json.dumps({'type':'comment','input':'comment'})
        )
        responsedata = json.loads(response.data.decode())

        self.assertEqual(response.status_code, 201)
        self.assertEqual(responsedata['data'][0]['message'], 'comment successfully added')

    def test_empty_type_media(self):

        response  = self.test_client.post(
            'ireporter/api/v2/red-flags/10/comments',
            content_type='application/json',
            headers=self.headers,
            data=json.dumps({'type':'','input':'comment'})
        )
        responsedata = json.loads(response.data.decode())

        self.assertEqual(response.status_code, 400)
        self.assertEqual(responsedata['error'], 'type should be a string')

    def test_wrong_type_media(self):

        response  = self.test_client.post(
            'ireporter/api/v2/red-flags/10/comments',
            content_type='application/json',
            headers=self.headers,
            data=json.dumps({'type':'joel','input':'comment'})
        )
        responsedata = json.loads(response.data.decode())

        self.assertEqual(response.status_code, 400)
        self.assertEqual(responsedata['error'], 'Valid types are video, image, and comment.')

    def test_wrong_input_media(self):

        response  = self.test_client.post(
            'ireporter/api/v2/red-flags/10/comments',
            content_type='application/json',
            headers=self.headers,
            data=json.dumps({'type':'comment','input':3})
        )
        responsedata = json.loads(response.data.decode())

        self.assertEqual(response.status_code, 400)
        self.assertEqual(responsedata['error'], 'Input should be a string')

    def test_no_flag_post_media(self):

        response  = self.test_client.post(
            'ireporter/api/v2/red-flags/1/comments',
            content_type='application/json',
            headers=self.headers,
            data=json.dumps({'type':'comment','input':'comment'})
        )
        responsedata = json.loads(response.data.decode())

        self.assertEqual(response.status_code, 404)
        self.assertEqual(responsedata['error'], "Redflag with id '1' not found")

    def test_no_flag_get_media(self):

        response  = self.test_client.get(
            'ireporter/api/v2/red-flags/1/comments',
            content_type='application/json'
        )
        responsedata = json.loads(response.data.decode())

        self.assertEqual(response.status_code, 404)
        self.assertEqual(responsedata['error'], "Redflag with id '1' not found")

    def test_get_comments(self):

        self.test_client.post(
            'ireporter/api/v2/red-flags/10/comments',
            content_type='application/json',
            headers=self.headers,
            data=json.dumps({'type':'comment','input':'comment'})
        )

        response = self.test_client.get(
            'ireporter/api/v2/red-flags/10/comments',
            content_type='application/json'
        )
        responsedata = json.loads(response.data.decode())

        self.assertEqual(response.status_code, 200)
        self.assertTrue('comment' in str(responsedata))

    def test_get_a_comment(self):

        resp = self.test_client.post(
            'ireporter/api/v2/red-flags/10/comments',
            content_type='application/json',
            headers=self.headers,
            data=json.dumps({'type':'comment','input':'comment'})
        )
        resp_data = json.loads(resp.data.decode())

        response = self.test_client.get(
            f'ireporter/api/v2/comments/{resp_data["data"][0]["id"]}',
            content_type='application/json'
        )
        responsedata = json.loads(response.data.decode())

        self.assertEqual(response.status_code, 200)
        self.assertTrue('comment' in str(responsedata))

    def test_update_a_comment(self):

        resp = self.test_client.post(
            'ireporter/api/v2/red-flags/10/comments',
            content_type='application/json',
            headers=self.headers,
            data=json.dumps({'type':'comment','input':'comment'})
        )
        resp_data = json.loads(resp.data.decode())

        self.test_client.put(
            f'ireporter/api/v2/comments/{resp_data["data"][0]["id"]}',
            content_type='application/json',
            headers=self.headers,
            data=json.dumps({'comment':'this is joel'})
        )

        response = self.test_client.get(
            f'ireporter/api/v2/comments/{resp_data["data"][0]["id"]}',
            content_type='application/json'
        )
        responsedata = json.loads(response.data.decode())

        self.assertEqual(response.status_code, 200)
        self.assertTrue('this is joel' in str(responsedata))

    def test_update_unauthorized(self):

        resp = self.test_client.post(
            'ireporter/api/v2/red-flags/10/comments',
            content_type='application/json',
            headers=self.headers,
            data=json.dumps({'type':'comment','input':'comment'})
        )
        resp_data = json.loads(resp.data.decode())

        response = self.test_client.post('/ireporter/api/v2/login', data=json.dumps({"username":"user", "password":"user"}), content_type='application/json')
        token = json.loads(response.data).get('access_token')

        response = self.test_client.put(
            f'ireporter/api/v2/comments/{resp_data["data"][0]["id"]}',
            headers={"Content-Type": "application/json", 'Authorization': f'Bearer {token}'},
            data=json.dumps({'comment':'this is joel'})
        )
        responsedata = json.loads(response.data.decode())

        self.assertEqual(response.status_code, 401)
        self.assertTrue('Sorry! you are not authorised to perform this action.' in str(responsedata))

    def test_update_wrong_comment_id(self):

        response = self.test_client.put(
            f'ireporter/api/v2/comments/0',
            headers=self.headers,
            data=json.dumps({'comment':'this is joel'})
        )
        responsedata = json.loads(response.data.decode())

        self.assertEqual(response.status_code, 404)
        self.assertTrue("Comment with id '0' not found" in str(responsedata))

    def test_update_no_comment(self):

        response = self.test_client.put(
            f'ireporter/api/v2/comments/0',
            headers=self.headers
        )
        responsedata = json.loads(response.data.decode())

        self.assertEqual(response.status_code, 400)
        self.assertTrue("No data posted" in str(responsedata))

    def test_update_wrong_comment(self):

        response = self.test_client.put(
            f'ireporter/api/v2/comments/0',
            headers=self.headers,
            data=json.dumps({'comment':1})
        )
        responsedata = json.loads(response.data.decode())

        self.assertEqual(response.status_code, 400)
        self.assertTrue("Comment should be a string" in str(responsedata))

    def test_delete_a_comment(self):

        resp = self.test_client.post(
            'ireporter/api/v2/red-flags/10/comments',
            content_type='application/json',
            headers=self.headers,
            data=json.dumps({'type':'comment','input':'comment'})
        )
        resp_data = json.loads(resp.data.decode())

        response = self.test_client.delete(
            f'ireporter/api/v2/comments/{resp_data["data"][0]["id"]}',
            content_type='application/json',
            headers=self.headers
        )
        responsedata = json.loads(response.data.decode())

        self.assertEqual(response.status_code, 200)
        self.assertTrue('Record successfully deleted' in str(responsedata))

    def test_delete_comment_unauthorized(self):

        resp = self.test_client.post(
            'ireporter/api/v2/red-flags/10/comments',
            content_type='application/json',
            headers=self.headers,
            data=json.dumps({'type':'comment','input':'comment'})
        )
        resp_data = json.loads(resp.data.decode())

        response = self.test_client.post('/ireporter/api/v2/login', data=json.dumps({"username":"user", "password":"user"}), content_type='application/json')
        token = json.loads(response.data).get('access_token')

        response = self.test_client.delete(
            f'ireporter/api/v2/comments/{resp_data["data"][0]["id"]}',
            headers={"Content-Type": "application/json", 'Authorization': f'Bearer {token}'}
        )
        responsedata = json.loads(response.data.decode())

        self.assertEqual(response.status_code, 401)
        self.assertTrue('Sorry! you are not authorised to perform this action.' in str(responsedata))

    def test_delete_missing_comment(self):

        response = self.test_client.delete(
            f'ireporter/api/v2/comments/0',
            headers=self.headers
        )
        responsedata = json.loads(response.data.decode())

        self.assertEqual(response.status_code, 404)
        self.assertTrue('Item not found' in str(responsedata))

    def test_missing_media(self):

        response = self.test_client.get(
            'ireporter/api/v2/red-flags/10/videos',
            content_type='application/json'
        )
        responsedata = json.loads(response.data.decode())

        self.assertEqual(response.status_code, 200)
        self.assertTrue('No data to display.' in str(responsedata))

    def test_missing_comment(self):

        response = self.test_client.get(
            'ireporter/api/v2/comments/0',
            content_type='application/json'
        )
        responsedata = json.loads(response.data.decode())

        self.assertEqual(response.status_code, 200)
        self.assertTrue('Sorry, resource not found.' in str(responsedata))
