import unittest
import webtest

from openprocurement.digital.signature import VERSION

config = {
    'password': '12345678',
}


class PrefixedRequestClass(webtest.app.TestRequest):
    @classmethod
    def blank(cls, path, *args, **kwargs):
        prefix = '/api/{}'.format(VERSION)

        if not path.startswith(prefix):
            path = prefix + path

        return webtest.app.TestRequest.blank(path, *args, **kwargs)


class BaseWebTest(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass
