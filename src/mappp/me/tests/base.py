import os
import unittest2

from pyramid import testing
import zope.testbrowser.wsgi


TESTINI = os.getenv('TESTINI')


class FunctionalLayer(object):

    def setUp(self):
        from paste.deploy import loadapp #@UnresolvedImport
        self.app = loadapp('config:%s#mappp.me' % TESTINI)
        threadlocals = dict(registry=self.app.registry, request=None)
        self.app.threadlocal_manager.push(threadlocals)

    setUp = classmethod(setUp)

    def tearDown(self):
        testing.tearDown()

    tearDown = classmethod(tearDown)


class TestBrowser(zope.testbrowser.wsgi.Browser):
    """A test browser which does not check robots.txt."""

    def __init__(self, *args, **kwargs):
        zope.testbrowser.wsgi.Browser.__init__(self, *args, **kwargs)
        self.mech_browser.set_handle_robots(False)

    def view(self): # pragma: no cover
        """ Convenience function to open html in the default browser.
            Can be used while writing tests:
            browser.send()
        """
        import webbrowser, tempfile, time
        with tempfile.NamedTemporaryFile(suffix='.html') as f:
            f.write(self.contents)
            f.flush()
            webbrowser.open(f.name)
            # give the os a chance to open the file before it's removed
            time.sleep(1)


class BrowserTestCase(unittest2.TestCase):

    def browser(self):
        return TestBrowser(wsgi_app=self.layer.app)
