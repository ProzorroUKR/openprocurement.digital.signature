# -*- coding: utf-8 -*-
from unittest import TestCase

from openprocurement.digital.signature.components.euscp import EUSignCP
from openprocurement.digital.signature.tests.base import config


class TestEuSCP(TestCase):
    def setUp(self):
        self.euscp = EUSignCP(config.get('password'))

    def tearDown(self):
        self.euscp.close()

    def test_b64encode(self):
        encoded_data = self.euscp.b64encode('test')
        self.assertEqual('dGVzdA==', encoded_data)

    def test_b64decode(self):
        decoded_data = self.euscp.b64decode('dGVzdA==')
        self.assertEqual('test', decoded_data)

    def test_enc_dec(self):
        self.assertTrue(self.euscp.client_session_is_initialized)
        self.assertTrue(self.euscp.server_session_is_initialized)

        signature = self.euscp.enc('test')

        self.assertTrue(len(signature) > 0)
        self.assertEqual(self.euscp.dec(signature), 'test')

