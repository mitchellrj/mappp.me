import mock
import unittest2

from mappp.me.tests.base import BrowserTestCase
from mappp.me.tests.base import FunctionalLayer


ANDROID_CHROME = (
    "Mozilla/5.0 (Linux; Android 4.0.4; GT-I9100 Build/IMM76L) "
    "AppleWebKit/535.19 (KHTML, like Gecko) Chrome/18.0.1025.166 "
    "Mobile Safari/535.19"
    )

DESKTOP_CHROME = (
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_4) "
    "AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.89 "
    "Safari/537.1"
    )


class TestAccessControl(unittest2.TestCase):
    
    layer = FunctionalLayer
        
    def _get_device(self, **kw):
        from mappp.me import accesscontrol
        
        environ = {'method': 'GET'}
        environ.update(kw)
        r = accesscontrol.EnhancedRequest(environ)
        
        return r.device
    
    def test_get_device_android(self):
        device = self._get_device(HTTP_USER_AGENT=ANDROID_CHROME)
        
        self.assertEqual(device.pointing_method, 'touchscreen')
    
    def test_get_device_desktop(self):
        device = self._get_device(HTTP_USER_AGENT=DESKTOP_CHROME)
        
        self.assertEqual(device.pointing_method, 'touchscreen')
        
    def test_get_device_opera_mini(self):
        device = self._get_decide(HTTP_USER_AGENT=DESKTOP_CHROME,
                                  HTTP_X_OPERAMINI_PHONE_UA=ANDROID_CHROME)
        
        self.assertEqual(device.pointing_method, 'touchscreen')