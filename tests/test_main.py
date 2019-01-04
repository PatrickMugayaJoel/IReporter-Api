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



    def test_user_register(self):
        user = {
                "firstname":"Joel",
                "lastname":"Mugaya",
                "username":"Josean",
                "email":"joel@joel.com",
                "phonenumber":256706084841,
                "password":"mugayajoel"
            }

        response  = self.test_client.post(
            'ireporter/api/v2/users',
            content_type='application/json',
            data=json.dumps(user)
        )
        responsedata = json.loads(response.data.decode())

        self.assertEqual(response.status_code, 201)
        self.assertEqual(responsedata['data'][0]['message'], 'Created User record')

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
            'ireporter/api/v2/users',
            content_type='application/json',
            data=json.dumps(user)
        )
        responsedata = json.loads(response.data.decode())

        self.assertEqual(response.status_code, 400)
        self.assertTrue('firstname can not be empty' in str(responsedata))

    def test_getusers(self):

        user = {
            "firstname":"Joel",
            "lastname":"Mugaya",
            "othernames":"Patrick",
            "username":"Josean",
            "email":"joel@joel.com",
            "phonenumber":256706084841,
            "password":"mugayajoel"
        }

        self.test_client.post(
            'ireporter/api/v2/users',
            content_type='application/json',
            data=json.dumps(user)
        )

        response  = self.test_client.get(
            'ireporter/api/v2/users',
            content_type='application/json'
        )
        responsedata = json.loads(response.data.decode())
        
        self.assertEqual(response.status_code, 200)
        self.assertTrue('joel@joel.com' in str(responsedata))


    def test_create_red_flag(self):

        response  = self.test_client.post(
            'ireporter/api/v2/red-flags',
            content_type='application/json',
            data=json.dumps(self.red_flag)
        )
        responsedata = json.loads(response.data.decode())

        self.assertEqual(response.status_code, 201)
        self.assertEqual(responsedata['data'][0]['message'], 'Created red-flag Record')

    def test_create_wrong_red_flag(self):

        red_flag = {
                "title":"Redflag",
                "type":"Redflag",
                "location":"7888876, 5667788",
                "images":"/flag.png",
                "videos":"/flag.mp4",
                "description":""
            }

        response  = self.test_client.post(
            'ireporter/api/v2/red-flags',
            content_type='application/json',
            data=json.dumps(red_flag)
        )
        responsedata = json.loads(response.data.decode())

        self.assertEqual(response.status_code, 400)
        self.assertEqual(responsedata['error'], ['description can not be empty.'])

    def test_get_red_flags(self):

        self.test_client.post(
            'ireporter/api/v2/red-flags',
            content_type='application/json',
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
            data=json.dumps(self.red_flag)
        )

        response = self.test_client.post(
            'ireporter/api/v2/red-flags',
            content_type='application/json',
            data=json.dumps(self.red_flag)
        )
        responsedata = json.loads(response.data.decode())

        self.assertEqual(response.status_code, 400)
        self.assertTrue('Incident already exists' in str(responsedata))

    def test_get_red_flag(self):

        resp = self.test_client.post(
            'ireporter/api/v2/red-flags',
            content_type='application/json',
            data=json.dumps(self.red_flag)
        )
        respdata = json.loads(resp.data.decode())

        response  = self.test_client.get(
            f'ireporter/api/v2/red-flags/{respdata["data"][0]["id"]}',
            content_type='application/json'
        )
        responsedata = json.loads(response.data.decode())

        self.assertEqual(response.status_code, 200)
        self.assertEqual(respdata["data"][0]["id"], responsedata["data"]['id'])

    def test_delete_red_flag(self):

        resp = self.test_client.post(
            'ireporter/api/v2/red-flags',
            content_type='application/json',
            data=json.dumps(self.red_flag)
        )
        respdata = json.loads(resp.data.decode())
        refflag_id = respdata["data"][0]["id"]

        response  = self.test_client.delete(
            f'ireporter/api/v2/red-flags/{refflag_id}',
            content_type='application/json'
        )

        response2  = self.test_client.get(
            f'ireporter/api/v2/red-flags/{refflag_id}',
            content_type='application/json'
        )
        responsedata = json.loads(response2.data.decode())

        self.assertEqual(response.status_code, 200)
        self.assertEqual(responsedata["error"], 'Redflag not found')

    def test_get_wrong_red_flag(self):

        response  = self.test_client.get(
            'ireporter/api/v2/red-flags/1',
            content_type='application/json'
        )
        responsedata = json.loads(response.data.decode())
        
        self.assertEqual(response.status_code, 404)
        self.assertEqual(responsedata['error'], 'Redflag not found')

    def test_put_redflag(self):

        red_flag2 = {
                    "title":"This is it",
                    "location":"123345, 98765",
                    "description":"desc"
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
        respdata2 = json.loads(response.data.decode())

        self.assertEqual(response.status_code, 200)
        self.assertEqual(respdata2['message'], 'Updated red-flag Record')

    def test_put_wrong_red_flag(self):

        response  = self.test_client.put(
            'ireporter/api/v2/red-flags/1',
            content_type='application/json'
        )
        respdata = json.loads(response.data.decode())

        self.assertEqual(response.status_code, 400)
        self.assertEqual(respdata['error'], 'No data was posted')
