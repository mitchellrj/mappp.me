import os
import sys

from mappp.me.models import BaseSession, DefaultIdFactory


session = BaseSession


class MemoryLimitedCache(dict):

    def __init__(self, *args, **kwargs):
        self.__max_bytes = kwargs.pop('max_bytes', sys.maxint)
        self._last_access_order = []
        dict.__init__(self, *args, **kwargs)

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
        return dict.__setitem__(self, key, value)

    def __getitem__(self, key):
        self._record_access(key)
        return dict.__getitem__(self, key)

    def __delitem__(self, key):
        if key in self._last_access_order:
            self._last_access_order.remove(key)
        return dict.__delitem__(self, key)


memory_cache = MemoryLimitedCache
ua_device_cache = MemoryLimitedCache(max_bytes=10*1024*1024)
_storage = None
default = object()


def get_storage():
    global _storage
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

    init_storage(settings['mappp.me.storage.location'],
                 expires=int(settings['mappp.me.storage.expires']),
                 gc_frequency=int(settings['mappp.me.storage.gc_frequency']))