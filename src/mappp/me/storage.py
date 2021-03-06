from threading import Lock, Thread
import time

from mappp.me.decorators import memoized


def gc(frequency, expires, storage):
    """Garbage collector thread, to periodically clear old sessions."""

    while 1:
        horizon = time.time() - expires

        storage.purge_before(horizon)

        time.sleep(frequency)


class BaseStorage(object):
    """Base storage object. Extended by the platform. Provides basic,
       multithreaded read/write consistency for sessions as well as
       memostorage clearing as required.
    """
    
    def __init__(self, expires, gc_frequency, id_factory):
        self.session_locks = {}
        self.id_factory = id_factory

        # Start up a garbage collector for this storage instance
        t = Thread(target=gc, name="mappp.me.storage.gc",
                   args=(gc_frequency, expires, self))
        t.daemon = True
        t.start()

    # Interface
    @memoized
    def get(self, session_id):
        raise NotImplemented

    @memoized
    def has(self, session_id):
        raise NotImplemented
    
    def _set(self, session_obj):
        raise NotImplemented
    
    def _remove(self, session_obj):
        raise NotImplemented

    # Consistency management
    def set(self, session):
        self._get_session_lock(session.id).acquire(True)
        self._get_session_lock(session.admin_id).acquire(True)
        self.get.reset(self, session.id)
        self.get.reset(self, session.admin_id)

        result = self._set(session)

        self._free_session_lock(session.id)
        self._free_session_lock(session.admin_id)

        return result

    def remove(self, session):
        session_id = session.id
        session_admin_id = session.admin_id
        self._get_session_lock(session_id).acquire(True)
        self._get_session_lock(session_admin_id).acquire(True)
        self.get.reset(self, session_id)
        self.get.reset(self, session_admin_id)
        self.has.reset(self, session_id)
        self.has.reset(self, session_admin_id)

        self._remove(session)

        self._free_session_lock(session_id)
        self._free_session_lock(session_admin_id)
        
    def _get_session_lock(self, session_id):
        if session_id not in self.session_locks:
            self.session_locks[session_id] = Lock()
        return self.session_locks[session_id]

    def _free_session_lock(self, session_id):
        if session_id not in self.session_locks:
            return
        self.session_locks[session_id].release()
        del self.session_locks[session_id]