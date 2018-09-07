# -*- coding: utf-8 -*-

# Main entry point

import logging.config
import pkg_resources


from openprocurement.digital.signature.utils import (
    Root, forbidden, request_params, add_logging_context, set_logging_context, set_renderer
)
from openprocurement.digital.signature.auth import authenticated_role

PKG = pkg_resources.get_distribution(__package__)
logger = logging.getLogger(PKG.project_name)

VERSION = '{}.{}'.format(
    int(PKG.parsed_version[0]), int(PKG.parsed_version[1]) if PKG.parsed_version[1].isdigit() else 0
)
ROUTE_PREFIX = '/api/{}'.format(VERSION)

def main(*args, **settings):
    from pyramid.config import Configurator
    from pyramid.events import NewRequest, ContextFound
    from pyramid.authentication import BasicAuthAuthenticationPolicy
    from pyramid.authorization import ACLAuthorizationPolicy
    from pyramid.renderers import JSON, JSONP

    logger.info('Start digital signature api, version {} ...'.format(VERSION))
    config = Configurator(
        autocommit=True,
        settings=settings,
        authentication_policy=BasicAuthAuthenticationPolicy(__name__),
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
    config.scan('openprocurement.digital.signature.api')
    return config.make_wsgi_app()