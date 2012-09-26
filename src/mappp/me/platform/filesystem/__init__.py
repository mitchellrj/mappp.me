import os
import sys
try:
    from UserDict import UserDict
except ImportError:
    from collections import UserDict

from mappp.me.models import BaseSession, DefaultIdFactory


session = BaseSession


class MemoryLimitedCache(UserDict):

    def __init__(self, *args, **kwargs):
        self.__max_bytes = kwargs.pop('max_bytes', sys.maxint)
        self._last_access_order = []
        UserDict.__init__(self, *args, **kwargs)

    def _prune(self):
        while sys.getsizeof(self) > self.__max_bytes and \
              self._last_access_order:
            del self[self._last_access_order.pop(0)]

    def _record_access(self, key):
        if key in self._last_access_order:
            self._last_access_order.remove(key)
        self._last_access_order.append(key)

    def __setitem__(self, key, value):
        self._prune()
        self._record_access(key)
        return UserDict.__setitem__(self, key, value)

    def __getitem__(self, key):
        self._record_access(key)
        return UserDict.__getitem__(self, key)

    def __delitem__(self, key):
        if key in self._last_access_order:
            self._last_access_order.remove(key)
        return UserDict.__delitem__(self, key)


# memcache class
memory_cache = MemoryLimitedCache
# 10MB cache for Wurfl device records
ua_device_cache = MemoryLimitedCache(max_bytes=10*1024*1024)
_storage = None
# Marker object
default = object()


def get_storage():
    if not _storage:
        raise RuntimeError("Storage not initialized.")
    return _storage


def init_storage(directory, expires=1800, gc_frequency=300,
                 id_factory=default):
    if id_factory is default:
        id_factory = DefaultIdFactory()
    global _storage
    from mappp.me.platform.filesystem.storage import SessionStorage
    _storage = SessionStorage(directory, expires, gc_frequency=gc_frequency,
                              id_factory=id_factory)


def init_platform_from_settings(settings):
    """Called by the app initializer in the root of the package."""

    init_storage(settings['mappp.me.storage.location'],
                 expires=int(settings['mappp.me.storage.expires']),
                 gc_frequency=int(settings['mappp.me.storage.gc_frequency']))