import cPickle
import os

from mappp.me.decorators import memoized
from mappp.me.storage import BaseStorage


class SessionStorage(BaseStorage):
    """Stores sessions in pickle files on the filesystem, with the
       filename of the session ID. A symlink is also created on session
       creation, pointing to the normal session ID.
       
       We don't need any querying or anything for this implementation.
       Pickling is comparatively fast.
    """

    def __init__(self, directory, expires, gc_frequency, id_factory):
        self.directory = directory
        super(SessionStorage, self).__init__(expires, gc_frequency, id_factory)

    def purge_before(self, horizon):
        """Called by the garbage collector thread. Should remove all
           sessions last modified before the horizon. Horizon in
           seconds since epoch.
        """
        
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
                # There's not really anything appropriate to do here.
                # We could perhaps email an administrator in future,
                # but we don't want to throw an error and crash the GC
                # thread.
                pass

    def list_all_ids(self):
        return os.listdir(self.directory)

    def validate_id(self, session_or_admin_id):
        """Validate the ID structurally. The Default ID factory doesn't
           allow anything that will get us in trouble.
        """
        
        return self.id_factory.validate_id(session_or_admin_id)

    def get_new_id(self, admin=False):
        """Generate IDs until we get one that isn't already taken.
        """
        
        id_ = None
        while not id_ or os.path.lexists(self._get_filename(id_)):
            id_ = self.id_factory(admin)

        return id_

    def _get_filename(self, session_id):
        """Gets absolute path of the data for the given session ID."""
        return os.path.join(self.directory, session_id)

    @memoized()
    def has(self, session_or_admin_id):
        filename = self._get_filename(session_or_admin_id)
        return os.path.lexists(filename)

    # Cache up to 20MB of sessions in RAM. This is a lot of sessions.
    @memoized(max_cache_bytes=20*1024*1024)
    def get(self, session_or_admin_id):
        filename = self._get_filename(session_or_admin_id)
        try:
            # open handles symlinks just fine.
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
        """Stores the given session object and sets up a symlink for
           the admin ID.
        """
        
        filename = self._get_filename(session.id)
        f = open(filename, 'w')
        cPickle.dump(session, f)
        f.close()
        admin_link = self._get_filename(session.admin_id)
        if not os.path.lexists(admin_link):
            os.symlink(filename, admin_link)

    def get_last_modified(self, session_or_admin_id):
        """Return the last modified time for the given ID in seconds
           since the epoch. Used by the garbage collector to purge.
        """
        
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
        """Extra remove function used by garbage collector."""
        
        fpath = os.path.join(self.directory, session_or_admin_id)
        os.unlink(fpath)

    def _remove(self, session):
        filename = self._get_filename(session.id)
        try:
            os.remove(filename)
        except:
            # There's not really anything appropriate to do here.
            # We could perhaps email an administrator in future,
            # but we don't want to throw an error.
            pass
        try:
            os.unlink(self._get_filename(session.admin_id))
        except:
            # Ditto.
            pass