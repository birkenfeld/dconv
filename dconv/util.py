"""
    d2d.util
    ~~~~~~~~

    :author: Georg Brandl
    :license: GPL
"""

import re, traceback

def make_character_class(chars):
    """Return a character class regex from a string of chars."""
    return '[' + re.escape(chars) + ']'


def fmt_ex(ex):
    """Format a single line with an exception description."""
    return traceback.format_exception_only(ex.__class__, ex)[-1].strip()


def xdir(o):
    """Like dir, but return only public names."""
    return [name for name in dir(o) if not name.startswith('_')]


class Namespace(dict):
    def __init__(self, *args, **kwds):
        self.__dict__.update(self)


class Record(tuple):
    def __new__(cls, args):
        obj = tuple.__new__(cls, (x[1] for x in args))
        obj.pairs = args
        for name, val in args:
            setattr(obj, name, val)
        return obj
