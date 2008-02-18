"""
    dconv.minifmt
    ~~~~~~~~~~~~~

    :author: Georg Brandl
    :license: GPL
"""


def str_v(x):
    if len(x) > 1 and x[0] == x[-1] and x[0] in '"\'':
        return eval(x)
    return x

def int_v(x):
    try:
        return int(x)
    except:
        return None

def choice_v(*vals):
    def validator(x):
        for v in vals:
            if x == v:
                return x
    return validator

def bool_v(x):
    if x.lower() in ('true', 'yes', '1'):
        return True
    return False

nodefault = object()


class FormatError(Exception):
    pass


class Minifmtable(object):
    properties = {}

    def __init__(self, **kwds):
        for prop, val in kwds.items():
            if prop in self.properties:
                self.set(prop, val)
            else:
                raise ValueError('invalid keyword argument: %s' % prop)

    @classmethod
    def fromstr(cls, source):
        self = cls()

        def err(msg):
            raise  '%s, line %d: %s' % (sourcename, i+1, msg)

        if isinstance(source, basestring):
            source = source.splitlines()
            sourcename = '<string>'
        else:
            sourcename = source.name

        for i, line in enumerate(source):
            line = line.strip()
            if not line or line.startswith('#'):
                continue

            try:
                prop, val = line.split(':', 1)
                prop = prop.rstrip()
                val = val.lstrip()
            except ValueError:
                err('invalid line, must be "property: value"')
                continue

            if prop not in cls.properties:
                err('invalid property %s' % prop)
                continue

            propspec = cls.properties[prop]
            valtype = propspec[0]
            if not isinstance(valtype, tuple):
                valtype = (valtype,)
            for stype in valtype:
                ret = stype(val)
                if ret is None:
                    continue
                if len(propspec) > 2 and propspec[2]:
                    self.multiset(prop, ret)
                else:
                    self.set(prop, ret)
                break
            else:
                err('invalid value for %s: %r' % (prop, val))

        for propname, propspec in cls.properties.items():
            if self.get(propname, None) is None:
                self.set(propname, propspec[1])

        return self


    def tostr(self, destination):
        # TODO.
        pass

    def get(self, prop, default=nodefault):
        if default is nodefault:
            return getattr(self, prop)
        return getattr(self, prop, default)

    def set(self, prop, val):
        setattr(self, prop, val)

    def multiset(self, prop, val):
        if not hasattr(self, prop):
            setattr(self, prop, [])
        getattr(self, prop).append(val)

    def __repr__(self):
        return '%s(%s)' % (
            self.__class__.__name__,
            ', '.join('%s=%r' % (p, self.get(p)) for p in self.properties))
