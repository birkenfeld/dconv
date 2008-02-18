"""
    dconv.cmdline
    ~~~~~~~~~~~~~

    :author: Georg Brandl
    :license: GPL
"""

import sys
import getopt

from dconv import convfile

def writemsg(msg):
    sys.stderr.write(msg + '\n')
    sys.stderr.flush()

usage = """\
Usage: d2d -i informat -o outformat infile
"""

def main(args):
    try:
        opts, args = getopt.getopt(args[1:], "hi:o:")
    except getopt.GetoptError, err:
        print >>sys.stderr, err
        print >>sys.stderr, usage
        return 1

    opts = dict(opts)
    if '-h' in opts or ('-i' not in opts or '-o' not in opts):
        print >>sys.stderr, usage
        return 1

    if len(args) > 1:
        print >>sys.stderr, usage
        return 1

    if not args or args[0] == '-':
        infile = sys.stdin
    else:
        infile = file(args[0])

    try:
        convfile(infile, sys.stdout, opts['-i'],
                 opts['-o'], writemsg, writemsg)
    except Exception, err:
        print >>sys.stderr, err
        return 1
    return 0
