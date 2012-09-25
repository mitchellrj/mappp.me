from mappp.me.platform.gae import session
from mappp.me.storage import BaseStorage


class GAESessionStorage(BaseStorage):

    def __init__(self, location, expires, gc_frequency, id_factory):
        super(GAESessionStorage, self).__init__(location, expires, gc_frequency, id_factory)
        self.location = location

    def purge_before(self, horizon):
        session.gql("WHERE last_updated < :1", horizon).delete()

    def validate_id(self, session_or_admin_id):
        return self.id_factory.validate_id(session_or_admin_id)

    def get_new_id(self, admin=False):
        id_ = None
        id_exists = lambda s: session.gql("WHERE _id = :1 OR _admin_id = :1", s).count()>0
        while not id_ or id_exists(id_):
            id_ = self.id_factory(admin)

        return id_

    def has(self, session_or_admin_id):
        return session.gql("WHERE _id = :1 OR _admin_id = :1",
                           session_or_admin_id).count()>0

    def get(self, session_or_admin_id):
        session = session.gql("WHERE _id = :1 OR _admin_id = :1",
                              session_or_admin_id).get()

    def _set(self, session):
        session.put()

    def _remove(self, session):
        session.delete()