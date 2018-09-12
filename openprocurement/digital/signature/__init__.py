# -*- coding: utf-8 -*-

# Main entry point

import os
import logging.config
import pkg_resources

from openprocurement.digital.signature.utils import (
    Root, forbidden, request_params, add_logging_context, set_logging_context, set_renderer, auth_check
)
from openprocurement.digital.signature.auth import authenticated_role
from openprocurement.digital.signature.utils import read_users

try:
    PKG = pkg_resources.get_distribution(__package__)
except pkg_resources.DistributionNotFound:
    logger = logging.getLogger(__name__)
    VERSION = '0.0'
else:
    logger = logging.getLogger(PKG.project_name)

    VERSION = '{}.{}'.format(
        int(PKG.parsed_version[0]), int(PKG.parsed_version[1]) if PKG.parsed_version[1].isdigit() else 0
    )

ROUTE_PREFIX = '/api/{}'.format(VERSION)
BASE_DIR = os.path.dirname(os.path.realpath(__file__))


def main(*args, **settings):
    from pyramid.config import Configurator
    from pyramid.events import NewRequest, ContextFound
    from pyramid.authentication import BasicAuthAuthenticationPolicy
    from pyramid.authorization import ACLAuthorizationPolicy
    from pyramid.renderers import JSON, JSONP

    logger.info('Start digital signature api, version {} ...'.format(VERSION))

    try:
        read_users(settings['auth.file'])
    except KeyError:
        pass

    config = Configurator(
        autocommit=True,
        settings=settings,
        authentication_policy=BasicAuthAuthenticationPolicy(auth_check, __name__),
        authorization_policy=ACLAuthorizationPolicy(),
        root_factory=Root,
        route_prefix=ROUTE_PREFIX
    )

    config.include('pyramid_exclog')
    config.add_forbidden_view(forbidden)
    config.add_request_method(request_params, 'params', reify=True)
    config.add_request_method(authenticated_role, reify=True)
    config.add_renderer('prettyjson', JSON(indent=4))
    config.add_renderer('jsonp', JSONP(param_name='opt_jsonp'))
    config.add_renderer('prettyjsonp', JSONP(indent=4, param_name='opt_jsonp'))
    config.add_subscriber(add_logging_context, NewRequest)
    config.add_subscriber(set_logging_context, ContextFound)
    config.add_subscriber(set_renderer, NewRequest)
    config.add_route('health', '/health')
    config.add_route('sign', '/sign')
    config.scan('openprocurement.digital.signature.api.views')
    return config.make_wsgi_app()