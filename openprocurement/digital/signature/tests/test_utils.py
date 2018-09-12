# -*- coding: utf-8 -*-
import os

from unittest import TestCase
from pyramid import testing
from webob.multidict import NestedMultiDict
from openprocurement.digital.signature import BASE_DIR
from openprocurement.digital.signature.utils import (
    auth_check, forbidden, request_params, read_users, USERS, error_handler
)


class TestUtils(TestCase):
    __test__ = True

    @classmethod
    def setUpClass(cls):
        pass

    def setUp(self):
        pass

    @classmethod
    def tearDownClass(cls):
        pass

    def tearDown(self):
        pass

    def test_auth_check(self):
        request = testing.DummyRequest()
        self.assertEqual(None, auth_check('test', 'test', request))

    def test_forbidden(self):
        request = testing.DummyRequest()
        response = forbidden(request)
        data = response.json_body
        self.assertEqual(response.status_code, 403)
        self.assertEqual(response.content_type, 'application/json')
        self.assertEqual(data.get('status'), 'error')
        self.assertEqual(
            data.get('errors')[0], {'location': 'url', 'name': 'permission', 'description': 'Forbidden'}
        )

    def test_request_params(self):
        request = testing.DummyRequest()
        self.assertEqual(request_params(request), NestedMultiDict())

        self.assertRaises(Exception, lambda: request_params(request.response))

    def test_read_users(self):
        self.assertEqual(USERS, {})
        read_users(os.path.join(BASE_DIR, 'tests', 'auth.ini'))
        self.assertIn('platform', USERS)
        self.assertEqual(USERS.get('platform'), {'password': '10', 'group': 'platforms'})

    def test_error_handler(self):
        request = testing.DummyRequest()
        self.assertEqual(
            error_handler(request, status=400, error={'location': 'url'}),
            {'status': 'error', 'errors': [{'location': 'url'}]}
        )





