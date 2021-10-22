import unittest
import requests


class ApiTest(unittest.TestCase):
    API_URL = 'http://127.0.0.1:5000/api/task'
    GET_URL = '{}/get_all'.format(API_URL)
    POST_URL = '{}/post'.format(API_URL)
    GET_ONE = '{}/get/'.format(API_URL)
    DELETE_URL = '{}/delete/'.format(API_URL)
    PUT_URL = '{}/put/'.format(API_URL)
    TASK_OBJ = {
        'title': 'Самотест Доавил это',
        'content': 'Самотест Доавил это'
    }

    TASK_OBJ_NEW = {
        'title': 'Самотест обновил это',
        'content': 'Самотест обновил это'
    }

    def test_1_get_all(self):
        r = requests.get(ApiTest.GET_URL)
        self.assertEqual(r.status_code, 200)

    def test_2_add_new_task(self):
        r = requests.post(ApiTest.POST_URL, json=ApiTest.TASK_OBJ)
        self.assertEqual(r.status_code, 200)

    def test_3_put_new_task(self):
        id = 1
        s = requests.put('{}{}'.format(ApiTest.PUT_URL, id), json=ApiTest.TASK_OBJ_NEW)
        self.assertEqual(s.status_code, 200)

    def test_4_get_new_task(self):
        id = 1
        r = requests.get('{}{}'.format(ApiTest.GET_ONE, id))
        self.assertEqual(r.status_code, 200)

    def test_5_delete_new_task(self):
        id = 1
        r = requests.delete('{}{}'.format(ApiTest.DELETE_URL, id))
        self.assertEqual(r.status_code, 200)
