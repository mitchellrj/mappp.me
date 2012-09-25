import datetime
import random

from mappp.me.platform import get_platform


class DefaultIdFactory(object):

    # alnum with lookalike characters removed
    chars = 'abcdefghjkmnopqrstuvwxzyABCDEFGHJKLMNPQRSTUVWXYZ23456789-_'

    def __call__(self, secure=False):
        id_ = ''
        size = 4  # ~10.5M combinations
        if secure:
            size = 14 # ~8E24 combinations
        for _ in range(size):
            id_ += random.choice(self.chars)
        return id_

    def validate_id(self, id_):
        for c in id_:
            if c not in self.chars:
                return False

        return True


class CustomTZ(datetime.tzinfo):

    def __init__(self, offset=None):
        self.offset = datetime.timedelta(minutes=(offset or 0) * -1)

    def utcoffset(self, dt):
        return self.offset

    def tzname(self, dt):
        return str(self.offset)

    def dst(self, dt):
        # Python docs say we can return None, but it is required by now()
        return datetime.timedelta()

    def localize(self, dt, is_dst=False):
        '''Convert naive time to local time'''
        if dt.tzinfo is not None:
            raise ValueError('Not naive datetime (tzinfo is already set)')
        return dt.replace(tzinfo=self)

    def normalize(self, dt, is_dst=False):
        '''Correct the timezone information on the given datetime'''
        if dt.tzinfo is None:
            raise ValueError('Naive time - no tzinfo set')
        return dt.replace(tzinfo=self)

    def __repr__(self):
        return "<Timezone offset %s>" % (self.offset,)

    def __str__(self):
        return str(self.offset)


class BaseSession(object):

    def __init__(self, longitude, latitude, tz=None):
        storage = get_platform().get_storage()
        self._id = storage.get_new_id()
        self._admin_id = storage.get_new_id(admin=True)
        self._tz = tz or 0
        self.longitude = longitude
        self.latitude = latitude
        self.last_updated = self.created = datetime.datetime.now(tz=self.tz)

    @property
    def id(self):
        return self._id

    @property
    def admin_id(self):
        return self._admin_id

    @property
    def tz(self):
        return CustomTZ(self._tz)

    def update(self, longitude, latitude):
        self.last_updated = datetime.datetime.now(tz=self.tz)
        self.longitude = longitude
        self.latitude = latitude