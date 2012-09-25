import os
import threading
import time
import sys

from pyramid.config import Configurator
import pyramid_beaker


def wurfl_monitor():
    last_mtime = time.time()
    while 1:
        try:
            if 'wurfl' in sys.modules and \
               os.stat(sys.modules.get('wurfl').__file__).st_mtime > last_mtime:
                # only possible to do it this way as wurfl.py has no complex
                # dependencies
                del sys.modules['wurfl']
        except:
            if 'wurfl' not in sys.modules:
                import wurfl

        time.sleep(600)


Settings = {}


def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """

    global Settings
    Settings = settings
    config = Configurator(settings=settings,
        root_factory='mappp.me.context.RootFactory',)
    config.include('pyramid_zcml')
    config.load_zcml('configure.zcml')

    from mappp.me.platform import set_platform
    platform = set_platform(settings.get('mappp.me.platform', 'filesystem'))
    platform.init_platform_from_settings(settings)

    from mappp.me.accesscontrol import EnhancedRequest, on_newrequest
    session_factory = pyramid_beaker.session_factory_from_settings(settings)
    config.set_session_factory(session_factory)
    config.set_request_factory(EnhancedRequest)
    config.add_subscriber(on_newrequest, 'pyramid.events.NewRequest')

    t = threading.Thread(target=wurfl_monitor, name="mappp.me.wurfl.updater")
    t.daemon = True
    t.start()

    return config.make_wsgi_app()