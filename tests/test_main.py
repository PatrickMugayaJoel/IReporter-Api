# import unittest
# from app import app
# import json
# from database.users_db import UsersDB
# from database.redflags_db import RedflagsDB

# class TestMain(unittest.TestCase):

#     def setUp(self):
#         self.test_client = app.test_client()
#         self.red_flag = {
#                     "title":"Redflag",
#                     "type":"Redflag",
#                     "location":"7888876, 5667788",
#                     "description":"description",
#                     "comment":"comment"
#                     }

#         self.user = {
#                     "firstname":"test",
#                     "lastname":"test",
#                     "username":"test",
#                     "email":"t@t.cm",
#                     "phonenumber":706084841,
#                     "password":"test"
#                 }

#         response_red_flag = self.test_client.post(
#             'ireporter/api/v2/red-flags',
#             content_type='application/json',
#             data=json.dumps(self.red_flag)
#         )
#         self.response_red_flag = json.loads(response_red_flag.data.decode())

#         response_user = self.test_client.post(
#             'ireporter/api/v2/users',
#             content_type='application/json',
#             data=json.dumps(self.user)
#         )
#         self.response_user = json.loads(response_user.data.decode())

#     def tearDown(self):
#         self.test_client.delete
#         db = UsersDB()
#         db.delete_user(self.response_user['data'][0]['id'])
#         db = RedflagsDB()
#         db.delete(self.response_red_flag['data'][0]['id'])



#     def test_create_red_flag(self):
#         red_flag = {
#                     "title":"test",
#                     "type":"Redflag",
#                     "location":"7888876, 5667788",
#                     "description":"description",
#                     "comment":"comment"
#                     }

#         response  = self.test_client.post(
#             'ireporter/api/v2/red-flags',
#             content_type='application/json',
#             data=json.dumps(red_flag)
#         )
#         responsedata = json.loads(response.data.decode())

#         self.assertEqual(response.status_code, 201)
#         self.assertEqual(responsedata['data'][0]['message'], 'Created red-flag Record')

#         db = RedflagsDB()
#         db.delete(responsedata['data'][0]['id'])

#     def test_get_red_flags(self):

#         response = self.test_client.get(
#             'ireporter/api/v2/red-flags',
#             content_type='application/json'
#         )
#         responsedata = json.loads(response.data.decode())

#         self.assertEqual(response.status_code, 200)
#         self.assertTrue('description' in str(responsedata))

#     def test_post_duplicate_red_flags(self):

#         self.test_client.post(
#             'ireporter/api/v2/red-flags',
#             content_type='application/json',
#             data=json.dumps(self.red_flag)
#         )

#         response = self.test_client.post(
#             'ireporter/api/v2/red-flags',
#             content_type='application/json',
#             data=json.dumps(self.red_flag)
#         )
#         responsedata = json.loads(response.data.decode())

#         self.assertEqual(response.status_code, 400)
#         self.assertTrue('Incident already exists' in str(responsedata))

#     def test_get_red_flag(self):

#         response  = self.test_client.get(
#             f'ireporter/api/v2/red-flags/{self.response_red_flag["data"][0]["id"]}',
#             content_type='application/json'
#         )
#         responsedata = json.loads(response.data.decode())

#         self.assertEqual(response.status_code, 200)
#         self.assertEqual(self.response_red_flag["data"][0]["id"], responsedata["data"]['flag_id'])

#     def test_delete_red_flag(self):

#         response = self.test_client.delete(
#             f"ireporter/api/v2/red-flags/{self.response_red_flag['data'][0]['id']}",
#             content_type='application/json'
#         )
#         responsedata = json.loads(response.data.decode())

#         self.assertEqual(response.status_code, 200)
#         self.assertEqual(responsedata["message"], 'Deleted red-flag Record')

#         response2 = self.test_client.get(
#             f"ireporter/api/v2/red-flags/{self.response_red_flag['data'][0]['id']}",
#             content_type='application/json'
#         )
#         responsedata = json.loads(response2.data.decode())

#         self.assertEqual(response2.status_code, 404)
#         self.assertEqual(responsedata["error"], 'Redflag not found')

#     def test_put_redflag(self):

#         red_flag2 = {
#                     "title":"This is it",
#                     "location":"123345, 98765",
#                     "description":"desc"
#                     }

#         response  = self.test_client.put(
#             f'ireporter/api/v2/red-flags/{self.response_red_flag["data"][0]["id"]}',
#             content_type='application/json',
#             data=json.dumps(red_flag2)
#         )
#         respdata2 = json.loads(response.data.decode())

#         self.assertEqual(response.status_code, 200)
#         self.assertEqual(respdata2['message'], 'Updated red-flag Record')

#     def test_put_red_flag_wrong(self):

#         red_flag2 = {
#                     "title":"Redflag",
#                     "location":"",
#                     "description":"description",
#                     "comment":"comment"
#                     }

#         response  = self.test_client.put(
#             f'ireporter/api/v2/red-flags/{self.response_red_flag["data"][0]["id"]}',
#             content_type='application/json',
#             data=json.dumps(red_flag2)
#         )
#         respdata = json.loads(response.data.decode())

#         self.assertEqual(response.status_code, 400)
#         self.assertTrue('location can not be empty.' in str(respdata['error']))
