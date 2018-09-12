# -*- coding: utf-8 -*-
from unittest import TestCase
from pyramid import testing
from openprocurement.digital.signature.api.views.health import health


class TestHealth(TestCase):
    def test_health(self):
        request = testing.DummyRequest()
        self.assertEqual(health(request).status_code, 200)
