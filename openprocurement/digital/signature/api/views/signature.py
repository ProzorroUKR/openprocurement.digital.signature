# -*- coding: utf-8 -*-

import json
import sys
import logging

from pyramid.view import view_config, view_defaults
from pyramid.response import Response

from openprocurement.digital.signature.components.euscp import EUSignCP

logger = logging.getLogger(__name__)

reload(sys)
sys.setdefaultencoding('utf-8')


@view_defaults(route_name='sign')
class SignView(object):
    def __init__(self, request):
        self.request = request
        self.psz_password = request.registry.settings.get('psz_password')

    @view_config(request_method='POST', renderer='json', permission='platform')
    def sign(self):
        data = self.request.json_body
        altchars = data.get('altchars')

        cp = EUSignCP(self.psz_password)
        signature = cp.enc(altchars)

        text = cp.dec(signature)
        cert_info = cp.cert_info

        body = json.dumps(
            {
                'altchars': altchars,
                'digitalSignature': signature,
                'text': text,
                'cert_info': {
                    'issuer': cert_info.get('pszIssuer'),
                    'serial': cert_info.get('pszSerial'),
                    'begin_time': cert_info.get('stCertBeginTime')
                }
            }
        )
        cp.close()

        return Response(body=body, content_type='application/json', status=200)

