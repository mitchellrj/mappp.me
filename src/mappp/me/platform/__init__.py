_platform = None


def get_platform():
    if not _platform:
        raise RuntimeError("Platform not initialized.")

    return _platform


def set_platform(id_):
    """Sets the platform to be whatever submodule of this is specified
       by the given id.
    """
    
    global _platform
    _platform = None
    try:
        _platform = __import__('mappp.me.platform.%s' % (id_,), fromlist=['*'])
    except ImportError, e:
        if id_ not in e.args:
            raise

    if not _platform:
        raise RuntimeError("Platform not available.")

    return _platform