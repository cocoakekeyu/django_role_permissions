# -*- coding: utf-8 -*-
from django.test import TestCase, Client


class PermissionTest(TestCase):

    def setUp(self):
        self.client = Client()

    def test_permission_list(self):
        response = self.client.get('/role/permission/', content_type='application/json')
        self.assertEqual(response.status_code, 200)
        print(response.content)
