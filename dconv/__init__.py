"""
    d2d data format conversion utility
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    :author: Georg Brandl
    :license: GPL
"""

import sys
import StringIO

from dconv.data import Data, InFormat, OutFormat, ReadError, WriteError
from dconv.minifmt import FormatError
from dconv import informats, outformats


def lookup(name, typ):
    if isinstance(name, typ):
        return name
    if not isinstance(name, str):
        raise FormatError("name must be %s or string" % typ.__name__)
    if typ is InFormat:
        if ':' in name:
            return InFormat.fromstr(name)
        elif '.' in name:
            return InFormat.fromstr(file(name))
        try:
            return InFormat.fromstr(getattr(informats, name))
        except AttributeError:
            raise FormatError("No in format %s." % name)
    elif typ is OutFormat:
        if ':' in name:
            return OutFormat.fromstr(name)
        elif '.' in name:
            return OutFormat.fromstr(file(name))
        try:
            return OutFormat.fromstr(getattr(outformats, name))
        except AttributeError:
            raise FormatError("No out format %s." % name)


def convfile(source, destination, informat, outformat,
             warnfunc, errfunc):
    try:
        informat = lookup(informat, InFormat)
        outformat = lookup(outformat, OutFormat)
    except FormatError, err:
        errfunc(str(err))
        return
    if informat is None or outformat is None:
        return

    try:
        data = Data.read(informat, source, warnfunc)
    except ReadError, err:
        errfunc(str(err))
        return
    try:
        data.write(outformat, destination, warnfunc)
    except WriteError, err:
        errfunc(str(err))


def conv(source, informat, outformat, warnfunc, errfunc):
    source = StringIO.StringIO(source)
    source.name = '<string>'
    destination = StringIO.StringIO()
    destination.name = '<string>'
    convfile(source, destination, informat, outformat)


if __name__ == '__main__':
    import d2d.cmdline
    sys.exit(d2d.cmdline.main(sys.argv))
