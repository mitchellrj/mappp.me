import os
import threading
import time
import sys

from pyramid.config import Configurator
import pyramid_beaker


# Global settings, a la Django :-/
Settings = {}


def main(global_config, **settings):
    """This function configures and returns a WSGI application."""

    global Settings
    Settings = settings
    config = Configurator(
        settings=settings,
        root_factory='mappp.me.context.RootFactory',)
    config.include('pyramid_zcml')
    config.load_zcml('configure.zcml')

    # set up storage
    from mappp.me.platform import set_platform
    platform = set_platform(settings.get('mappp.me.platform', 'filesystem'))
    platform.init_platform_from_settings(settings)

    from mappp.me.accesscontrol import EnhancedRequest, on_newrequest
    session_factory = pyramid_beaker.session_factory_from_settings(settings)
    config.set_session_factory(session_factory)
    config.set_request_factory(EnhancedRequest)
    config.add_subscriber(on_newrequest, 'pyramid.events.NewRequest')

    return config.make_wsgi_app()