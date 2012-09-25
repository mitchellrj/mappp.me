from threading import Lock, Thread
import time


def gc(frequency, expires, storage):

    while 1:
        horizon = time.time() - expires

        storage.purge_before(horizon)

        time.sleep(frequency)


class BaseStorage(object):
    def __init__(self, location, expires, gc_frequency, id_factory):
        self.session_locks = {}
        self.id_factory = id_factory

        t = Thread(target=gc, name="mappp.me.storage.gc",
                   args=(gc_frequency, expires, self))
        t.daemon = True
        t.start()

    def _get_session_lock(self, session_id):
        if session_id not in self.session_locks:
            self.session_locks[session_id] = Lock()
        return self.session_locks[session_id]

    def _free_session_lock(self, session_id):
        if session_id not in self.session_locks:
            return
        self.session_locks[session_id].release()
        del self.session_locks[session_id]

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