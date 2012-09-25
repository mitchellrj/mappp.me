from google.appengine.api import memcache
from google.appengine.ext import db

from mappp.me.models import BaseSession, DefaultIdFactory


class GAESession(db.Model, BaseSession):
    _id = db.StringProperty(indexed=True)
    _admin_id = db.StringProperty(indexed=True)
    _tz = db.IntegerProperty()
    longitude = db.FloatProperty()
    latitude = db.FloatProperty()
    last_updated = db.DateTimeProperty(auto_now=True)
    created = db.DateTimeProperty(auto_now_add=True)


session = GAESession


class GAEMemoizeCache(object):

    def __init__(self, *args, **kwargs):
        self.__cache = memcache

    def __setitem__(self, key, value):
        return self.__cache.set(key, value)

    def __getitem__(self, key):
        return self.__cache.get(self, key)

    def __delitem__(self, key):
        self.__cache.delete(key)

memory_cache = GAEMemoizeCache
ua_device_cache = GAEMemoizeCache()
_storage = None


def get_storage():
    global _storage
    if not _storage:
        raise RuntimeError("Storage not initialized.")
    return _storage


default = object()


def init_storage(location, expires=1800, gc_frequency=300,
                 id_factory=default):
    global _storage
    if id_factory is default:
        id_factory = DefaultIdFactory()

    from mappp.me.platform.gae.storage import GAESessionStorage
    _storage = GAESessionStorage(location, expires, gc_frequency, id_factory)


def init_platform_from_settings(settings):

    init_storage(settings['mappp.me.storage.location'],
                 expires=int(settings['mappp.me.storage.expires']),
                 gc_frequency=int(settings['mappp.me.storage.gc_frequency']))