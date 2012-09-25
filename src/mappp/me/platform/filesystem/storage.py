import cPickle
import os

from mappp.me.decorators import memoized
from mappp.me.storage import BaseStorage


class SessionStorage(BaseStorage):

    def __init__(self, directory, expires, gc_frequency, id_factory):
        self.directory = directory
        super(SessionStorage, self).__init__(directory, expires, gc_frequency, id_factory)

    def purge_before(self, horizon):
        for id_ in self.list_all_ids():
            try:
                self._get_session_lock(id_).acquire(True)
                last_modified = self.get_last_modified(id_)

                if last_modified and last_modified < horizon:
                    self._remove_by_id(id_)
                    self.get.reset(self, id_)
                    self.has.reset(self, id_)

                self._free_session_lock(id_)
            except:
                pass

    def list_all_ids(self):
        return os.listdir(self.directory)

    def validate_id(self, session_or_admin_id):
        return self.id_factory.validate_id(session_or_admin_id)

    def get_new_id(self, admin=False):
        id_ = None
        while not id_ or os.path.lexists(self._get_filename(id_)):
            id_ = self.id_factory(admin)

        return id_

    def _get_filename(self, session_id):
        return os.path.join(self.directory, session_id)

    @memoized()
    def has(self, session_or_admin_id):
        filename = self._get_filename(session_or_admin_id)
        return os.path.lexists(filename)

    @memoized(max_cache_bytes=20*1024*1024)
    def get(self, session_or_admin_id):
        filename = self._get_filename(session_or_admin_id)
        try:
            f = open(filename, 'r')
            result = cPickle.load(f)
            f.close()
            return result
        except:
            try:
                os.remove(filename)
            except:
                pass
            return None

    def _set(self, session):
        filename = self._get_filename(session.id)
        f = open(filename, 'w')
        cPickle.dump(session, f)
        f.close()
        admin_link = self._get_filename(session.admin_id)
        if not os.path.lexists(admin_link):
            os.symlink(filename, admin_link)

    def get_last_modified(self, session_or_admin_id):
        fpath = os.path.join(self.directory, session_or_admin_id)
        if os.path.islink(fpath):
            target = os.readlink(fpath)
            if not os.path.exists(target):
                return None
            else:
                return os.stat(target).st_mtime
        else:
            return os.stat(fpath).st_mtime

    def _remove_by_id(self, session_or_admin_id):
        fpath = os.path.join(self.directory, session_or_admin_id)
        os.unlink(fpath)

    def _remove(self, session):
        filename = self._get_filename(session.id)
        try:
            os.remove(filename)
        except:
            pass
        try:
            os.unlink(self._get_filename(session.admin_id))
        except:
            pass