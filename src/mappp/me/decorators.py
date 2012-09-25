import functools
import sys

from pyramid.decorator import reify

from mappp.me.platform import get_platform


# http://wiki.python.org/moin/PythonDecoratorLibrary#Memoize
class memoized(object):
    """Decorator that caches a function's return value each time it is called.
    If called later with the same arguments, the cached value is returned, and
    not re-evaluated.
    """
    def __init__(self, keyer=None, max_cache_bytes=None):
        self.cache_size = max_cache_bytes or sys.maxint
        self.keyer = None

    @reify
    def cache(self):
        # Defer creation of cache so we may create the platform first
        return get_platform().memory_cache(max_bytes=self.cache_size)

    def __call__(self, func):

        class inner(object):

            def __init__(self, memoizer):
                self.memoizer = memoizer

            def _reset(self, *args):
                if not args:
                    self.memoizer.cache = {}

                elif args in self.memoizer.cache:
                    del self.memoizer.cache[args]

            def __get__(self, obj, objtype):
                fn = functools.partial(self.__call__, obj)
                fn.reset = self._reset
                return fn

            def __call__(self, *args, **kwargs):
                key = args
                if self.memoizer.keyer:
                    key = self.memoizer.keyer(args)
                try:
                    return self.memoizer.cache[key]
                except KeyError:
                    value = func(*args)
                    self.memoizer.cache[key] = value
                    return value
                except TypeError:
                    # uncachable -- for instance, passing a list as an argument.
                    # Better to not cache than to blow up entirely.
                    return func(*args)

        return inner(self)

    def __repr__(self):
        """Return the function's docstring."""
        return self.func.__doc__