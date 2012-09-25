import datetime
from time import mktime
from urllib import quote
from wsgiref.handlers import format_date_time

from pyramid.httpexceptions import HTTPException, HTTPFound
from pyramid.renderers import get_renderer, render_to_response
from pyramid.security import has_permission

from mappp.me import Settings as settings
from mappp.me.platform import get_platform


class DeviceCss(object):
    def __init__(self, request):
        self.request = request

    def __call__(self):
        self.request.response.content_type = "text/css"
        self.request.response.cache_control = 'private max-age=3600 s-maxage=0'
        return {'device': self.request.device}


class BaseView(object):

    def populate(self, request):
        return dict()

    def __init__(self, request):
        self.request = request

    def __call__(self, *args, **kwargs):
        page_width = min(self.request.device.resolution_width,
                         self.request.device.max_image_width)
        values = dict(
            main = get_renderer('templates/master.pt').implementation(),
            context = getattr(self.request, 'context', None),
            request = self.request,
            js_api_key = settings.get('mappp.me.google.js_api_key', ''),
            maps_api_key = settings.get('mappp.me.gmaps.api_key', ''),
            page_width = page_width,
            image_size = (page_width>1024 and '') or
                         (page_width>512 and 'medium-') or
                         (page_width>256 and 'small-') or
                         'tiny-'
        )
        values.update(self.populate(self.request))
        exception = getattr(self.request, 'exception', None)
        if exception and isinstance(exception, HTTPException):
            self.request.response.status_int = exception.code
        return values.get('response') or values


class FrontPageView(BaseView):

    pass


class NewSessionView(BaseView):

    def __call__(self):
        long = self.request.params.get('longitude')
        lat = self.request.params.get('latitude')
        try:
            tz = int(self.request.params.get('tz', 0))
        except (TypeError, ValueError):
            tz = 0

        session = get_platform().session(long, lat, tz=tz)
        get_platform().get_storage().set(session)

        new_session_url = '%s/%s' % (self.request.application_url,
                                     session.admin_id)

        cookie_age = int(settings.get('mappp.me.storage.expires', 0))

        new_cookie = session.admin_id
        if self.request.existing_sessions:
            new_cookie = ','.join(self.request.existing_sessions +
                                  [session.admin_id])

        self.request.response.set_cookie('mappp',
                            new_cookie,
                            max_age=cookie_age,
                            httponly=True)

        # for older browsers
        self.request.response.content_type = 'text/plain'

        return {'admin_link': new_session_url}


class SessionView(BaseView):

    def populate(self, request):
        is_wml = request.environ.get('PATH_INFO', '').endswith('.wml')

        if not is_wml and \
           'text/vnd.wap.wml' in request.accept and \
           request.accept.best_match(['text/html',
                                      'application/json',
                                      'text/javascript',
                                      'application/xhtml+xml',
                                      'text/vnd.wap.wml',
                                      ])=='text/vnd.wap.wml':
            wml_uri = '%s/%s.wml' % (request.application_url,
                                     request.context.id)
            raise HTTPFound(location=wml_uri)

        is_owner = bool(has_permission('owner', request.context, request))

        today = datetime.datetime.now(tz=request.context.tz).replace(hour=0, minute=0, second=0, microsecond=0)
        created = request.context.created
        created_text = created.strftime('%H:%M')
        if created < today:
            diff = today - created
            if diff > datetime.timedelta(days=1):
                created_text = '%s %s days ago' % (created_text, diff.days)
            else:
                created_text = '%s yesterday' % (created_text,)
        else:
            created_text = '%s today' % (created_text,)

        zoom = 13
        if False not in [c.isdigit() for c in request.params.get('zoom', 'foo')] or \
           False not in [c.isdigit() for c in request.cookies.get('zoom', 'foo')]:
            zoom = int(request.params.get('zoom') or request.cookies.get('zoom'))

        map_upgrade = False
#        map_upgrade = request.supports_javascript and \
#                      request.device.resolution_width>=600 and \
#                      (
#                          request.device.is_tablet or
#                          request.device.wifi or
#                          request.device.brand_name=='Desktop' or
#                          not request.device.mobile_browser
#                      )

        result = {'is_owner': is_owner,
                  'latitude': request.context.latitude,
                  'longitude': request.context.longitude,
                  'created': created_text,
                  'sms_link': '',
                  #'marker_style': 'icon:' + quote(request.static_url('mappp.me:static/images/pointer-small-filled-transparent.png')),
                  'marker_style': quote('color:white|size:med'),
                  'quoted_uri': quote('%s%s' % (request.application_url, request.path)),
                  'zoom': zoom,
                  'map_upgrade': map_upgrade
                  }

        send_string = request.device.xhtml_send_sms_string
        if send_string!=u'none':
            if request.device.mobile_browser!=u'Android Webkit':
                # workaround for:
                # http://code.google.com/p/android/issues/detail?id=11451
                # http://code.google.com/p/android/issues/detail?id=12142
                # http://code.google.com/p/android/issues/detail?id=15866
                result['sms_link'] = '%s?body=%s' % (send_string,
                                                     quote('Find me at %s/%s .' %
                                                           (request.application_url,
                                                            request.context.id)))

        if request.method=='POST' and is_owner:

            long = float(request.params.get('longitude'))
            lat = float(request.params.get('latitude'))

            request.context.update(long, lat)

            get_platform().get_storage().set(request.context)

            result.update({'latitude': lat,
                           'longitude': long})

        last_updated = request.context.last_updated.astimezone(request.context.tz)
        result['last_updated'] = last_updated.strftime('%H:%M')
        expires = (last_updated + datetime.timedelta(minutes=30)).astimezone(request.context.tz)
        result['expires'] = format_date_time(mktime(expires.timetuple()))
        request.response.expires = expires
        request.response.last_modified = last_updated
        request.response.cache_control = 'no-cache'

        if request.method=='POST' and is_owner:

            result['response'] = render_to_response('json', result,
                                                    request=request)

            if request.existing_sessions:
                # reset the ages
                cookie_age = int(settings.get('mappp.me.storage.expires', 0))

                self.request.response.set_cookie('mappp',
                                                 ','.join(request.existing_sessions),
                                                 max_age=cookie_age,
                                                 httponly=True)

        if is_wml:
            request.response.content_type = 'text/vnd.wap.wml'

        return result


class DeleteSessionView(BaseView):

    def __call__(self):
        get_platform().get_storage().remove(self.request.context)
        self.request.response.delete_cookie('mappp')

        front_page_url = '%s/' % (self.request.application_url,)

        raise HTTPFound(location=front_page_url)