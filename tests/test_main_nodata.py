import unittest
from app import app
import json

class TestMainNoData(unittest.TestCase):

    def setUp(self):
        self.test_client = app.test_client()
        self.red_flag = {
                    "title":"Redflag",
                    "type":"Redflag",
                    "location":"7888876, 5667788",
                    "description":"",
                    "comment":"comment"
                    }

    def tearDown(self):
        self.test_client.delete



    def test_create_wrong_red_flag(self):

        response  = self.test_client.post(
            'ireporter/api/v2/red-flags',
            content_type='application/json',
            data=json.dumps(self.red_flag)
        )
        responsedata = json.loads(response.data.decode())

        self.assertEqual(response.status_code, 400)
        self.assertEqual(responsedata['error'], ['description can not be empty.'])

    def test_create_empty_red_flag(self):

        response  = self.test_client.post(
            'ireporter/api/v2/red-flags',
            content_type='application/json'
        )

        responsedata = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 400)
        self.assertEqual(responsedata['error'], 'No data was posted')

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

    def test_put_red_flag_wrong2(self):

        response  = self.test_client.put(
            'ireporter/api/v2/red-flags/1',
            content_type='application/json',
            data=json.dumps(self.red_flag)
        )
        respdata = json.loads(response.data.decode())

        self.assertEqual(response.status_code, 404)
        self.assertEqual(respdata['error'], 'Redflag not found')
