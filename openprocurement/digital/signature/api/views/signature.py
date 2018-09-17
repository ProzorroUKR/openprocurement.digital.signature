# -*- coding: utf-8 -*-

import json
import sys
import logging

from pyramid.view import view_config, view_defaults
from pyramid.response import Response

from openprocurement.digital.signature.components.euscp import EUSignCP
from openprocurement.digital.signature.utils import uid, context_unpack
from openprocurement.digital.signature.journal_msg_ids import API_REQUIRED_FIELDS, API_INFO

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
        sign_data = data.get('sign_data')

        session_id = uid()

        if sign_data:

            euscp = EUSignCP(self.psz_password)

            logger.info('Session id: {}'.format(session_id), extra=context_unpack(
                request=self.request, msg={'MESSAGE_ID': API_INFO}
            ))

            signature = euscp.enc(sign_data)
            cert_info = euscp.cert_info

            body = json.dumps(
                {
                    'id': session_id,
                    'sign_data': sign_data,
                    'signature': signature,
                    'cert_info': {
                        'issuer': cert_info.get('pszIssuer'),
                        'serial': cert_info.get('pszSerial'),
                        'begin_time': cert_info.get('stCertBeginTime')
                    }
                }
            )
            euscp.close()
        else:
            body = json.dumps({'success': False, 'error': True, 'message': '\'sign_data\' field is required'})

            logger.warn(
                '\'sign_data\' field is required', extra=context_unpack(
                    request=self.request, msg={'MESSAGE_ID': API_REQUIRED_FIELDS}, params={'SESSION_ID': session_id}
                )
            )

        return Response(body=body, content_type='application/json', status=400)

