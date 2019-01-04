import unittest
from app import app
import json


class TestUsers(unittest.TestCase):

    def setUp(self):
        self.test_client = app.test_client()
        self.test_client.get('/clearusers')
        self.test_client.get('/clearflagss')
        self.red_flag = {
                    "title":"Redflag",
                    "type":"Redflag",
                    "location":"7888876, 5667788",
                    "description":"description",
                    "comment":"comment"
                    }


    def test_home(self):

        response  = self.test_client.get('/')
        responsedata = json.loads(response.data.decode())

        self.assertEqual(response.status_code, 200)
        self.assertTrue('welcome', str(responsedata))

    def test_errorpage(self):

        response  = self.test_client.get('/joel')
        responsedata = json.loads(response.data.decode())

        self.assertEqual(response.status_code, 404)
        self.assertTrue('You have entered an unknown URL.', str(responsedata))

    def test_user_register(self):

        response  = self.test_client.post(
            'ireporter/api/v2/users',
            content_type='application/json'
        )

        responsedata = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 400)
        self.assertEqual(responsedata['error'], 'No data posted')

    def test_create_red_flag(self):

        response  = self.test_client.post(
            'ireporter/api/v2/red-flags',
            content_type='application/json'
        )

        responsedata = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 400)
        self.assertEqual(responsedata['error'], 'No data was posted')

    def test_getusers(self):

        response  = self.test_client.get(
            'ireporter/api/v2/users',
            content_type='application/json'
        )

        responsedata = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 404)
        self.assertEqual(responsedata['error'], 'No Users found')

    def test_get_red_flags(self):

        response  = self.test_client.get(
            'ireporter/api/v2/red-flags',
            content_type='application/json'
        )

        responsedata = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 404)
        self.assertEqual(responsedata['error'], 'No redflags found')

    def test_get_red_flag(self):

        response  = self.test_client.get(
            'ireporter/api/v2/red-flags/1',
            content_type='application/json'
        )

        responsedata = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 404)
        self.assertEqual(responsedata['error'], 'Redflag not found')

    def test_delete_red_flag(self):

        response  = self.test_client.delete(
            'ireporter/api/v2/red-flags/1',
            content_type='application/json'
        )

        responsedata = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 404)
        self.assertEqual(responsedata['error'], 'Redflag not found')


    def test_put_red_flag_wrong(self):

        red_flag2 = {
                    "title":"Redflag",
                    "location":"",
                    "description":"description",
                    "comment":"comment"
                    }

        resp = self.test_client.post(
            'ireporter/api/v2/red-flags',
            content_type='application/json',
            data=json.dumps(self.red_flag)
        )
        respdata = json.loads(resp.data.decode())

        response  = self.test_client.put(
            f'ireporter/api/v2/red-flags/{respdata["data"][0]["id"]}',
            content_type='application/json',
            data=json.dumps(red_flag2)
        )
        respdata = json.loads(response.data.decode())

        self.assertEqual(response.status_code, 400)
        self.assertTrue('location can not be empty.' in str(respdata['error']))

    def test_put_red_flag_wrong2(self):

        response  = self.test_client.put(
            'ireporter/api/v2/red-flags/1',
            content_type='application/json',
            data=json.dumps(self.red_flag)
        )
        respdata = json.loads(response.data.decode())

        self.assertEqual(response.status_code, 404)
        self.assertEqual(respdata['error'], 'Redflag not found')

