from pyramid.exceptions import NotFound
from pyramid.security import Allow, Everyone

from mappp.me.platform import get_platform


class RootFactory(object):
    """The root context."""
    __acl__ = [ (Allow, Everyone, 'view'), ]

    def __init__(self, request):
        self.request = request


def SessionFactory(request):
    """Loads a session as the context and applies permissions."""
    
    acl = [(Allow, Everyone, 'view')]

    session_id = request.matchdict.get('session')
    session = get_platform().get_storage().get(session_id)

    if not session:
        raise NotFound('No such session')

    is_admin_link = session_id==session.admin_id

    if is_admin_link:
        acl += [(Allow, Everyone, 'owner')]

    session.__acl__ = acl
    return session