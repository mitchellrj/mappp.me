from pyramid.decorator import reify
from pyramid.request import Request
from pywurfl.algorithms import TwoStepAnalysis
from wurfl import devices

from mappp.me.platform import get_platform


_ua_device_cache = get_platform().ua_device_cache


def on_newrequest(event):
    """Fix the https bug in Pyramid / Paste."""
    
    if 'HTTP_X_VHM_ROOT' in event.request.environ:
        event.request.environ['wsgi.url_scheme'] = 'https'


class EnhancedRequest(Request):

    @reify
    def device(self):
        """Look up the device profile based on the UA and cache it on
           the request object.
        """
        
        global _ua_device_cache
        ua = unicode(self.user_agent)

        if "HTTP_X_OPERAMINI_PHONE_UA" in self.environ:
            # Opera mini proxy specia case
            ua = unicode(self.environ["HTTP_X_OPERAMINI_PHONE_UA"])

        if ua not in _ua_device_cache:
            search_algorithm = TwoStepAnalysis(devices)
            _ua_device_cache[ua] = devices.select_ua(ua, search=search_algorithm)

        return _ua_device_cache[ua]

    @reify
    def supports_javascript(self):
        """Simple test if the device supports all the JavaScript
           features we require.
        """
        
        device = self.device
        return device.ajax_support_javascript and \
               device.ajax_support_getelementbyid and \
               device.ajax_manipulate_dom and \
               device.ajax_manipulate_css and \
               device.ajax_support_events and \
               device.ajax_support_event_listener

    @reify
    def existing_sessions(self):
        """Get a list of mappps that are currently valid for this
           browser session.
        """
        
        existing_sessions = self.cookies.get('mappp')
        if existing_sessions:
            sessions = []
            storage = get_platform().get_storage()
            for session in existing_sessions.split(','):
                if storage.has(session):
                    sessions.append(session)
            if sessions:
                return sessions

            self.response.delete_cookie('mappp')

        return []