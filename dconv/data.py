"""
    dconv.data
    ~~~~~~~~~~

    :author: Georg Brandl
    :license: GPL
"""

import sys
import re
from string import Template

from dconv.minifmt import *
from dconv.util import make_character_class, fmt_ex, Record, Namespace


class InFormat(Minifmtable):
    """The format for input format descriptions."""

    properties = {
        'defs': (choice_v('auto', 'none', 'colon', 'equals'),
                 'none'),
        'skip_until': (str_v, None),
        'extra_skip': (int_v, None),
        'headers': (str_v, [], 1),
        'end': ((choice_v('auto'), str_v), 'auto'),
        'comments': ((choice_v('none'), str_v), 'none'),
        'fields': ((choice_v('auto'), str_v), 'auto'),
        'fieldsep': (str_v, ' \t'),
        'linejunk': (str_v, [], 1),
        'fieldregex': (str_v, None),
    }


class OutFormat(Minifmtable):
    """The format for output format descriptions."""

    properties = {
        'fieldnames': (str_v, ''),
        'module': (str_v, [], 1),
        'assertion': (str_v, [], 1),
        'const': (str_v, [], 1),
        'condition': (str_v, [], 1),
        'field': (str_v, [], 1),
        'outfields': (str_v, [], 1),
        'outfieldsexp': (str_v, [], 1),
        'headers': (bool_v, False),
        'fieldsep': (str_v, '\t'),
        'prologue': (str_v, [], 1),
        'epilogue': (str_v, [], 1),
    }


class ReadError(Exception):
    """Raised when reading a file fails."""
    pass

class WriteError(Exception):
    """Raised when writing a file fails."""
    pass


class Data(object):
    """This object holds everything read from an input file."""

    def __init__(self, sourcename):
        self.sourcename = sourcename

        self.data = []
        self.numrecords = 0
        self.numfields = 0
        self.headers = {}
        self.defs = {}
        self.skipped = []

    @classmethod
    def read(cls, fmt, source, warnfunc=None, sourcename=None):
        """
        Read data formatted as `fmt` from file object `source`.  Use `warnfunc`
        to emit warnings. `sourcename` can be given if `source.name` isn't
        helpful (the source name is included in error and warning messages).
        """
        # Create an instance of Data
        self = cls(sourcename or source.name)

        def err(msg):
            raise ReadError('%s, line %d: %s' % (self.sourcename, i, msg))

        def warn(msg):
            if warnfunc:
                warnfunc('%s, line %d: %s' % (self.sourcename, i, msg))

        # The fields are either specified by a regex with a number of groups,
        # or by a string of single characters at which splitting should occur.
        if fmt.fieldregex:
            regex = re.compile(fmt.fieldregex)
            def splitline(line):
                return regex.match(line).groups()
        else:
            junk = set(fmt.linejunk)
            regex = re.compile(make_character_class(fmt.fieldsep))
            def splitline(line):
                split = regex.split(line)
                return [part for part in split
                        if part and part not in junk]

        def add_def(line, sep):
            """Look for a definition in the line, and parse it."""
            try:
                name, value = line.split(sep, 1)
            except:
                return
            else:
                name = name.strip().replace(' ', '_')
                value = value.strip()
                try:
                    num, unit = value.split(None, 1)
                    value = float(num)
                except ValueError:
                    pass
                self.defs[name.strip()] = value

        # `skipping` can be
        # * 0   if skipping is over
        # * -1  if still looking for `skip_until` string
        # * a positive number if in `extra_skip` phase
        skipping = 0
        if fmt.skip_until or fmt.extra_skip:
            skipping = fmt.extra_skip
            if fmt.skip_until:
                skipping = -1
        i = 0
        restheaders = fmt.headers[::-1]
        for line in source:
            i += 1
            line = line.rstrip()
            if fmt.comments != 'none':
                if line.lstrip().startswith(fmt.comments):
                    continue
            if skipping:
                if skipping == -1:
                    if fmt.skip_until in line:
                        if fmt.extra_skip:
                            skipping = fmt.extra_skip
                            continue
                        else:
                            skipping = 0
                else:
                    skipping -= 1

            if skipping:
                if fmt.defs == 'colon' or fmt.defs == 'auto':
                    add_def(line, ':')
                if fmt.defs == 'equals' or fmt.defs == 'auto':
                    add_def(line, '=')
                self.skipped.append(line)
                continue

            if restheaders:
                split = splitline(line)
                if not self.numfields:
                    self.numfields = len(split)
                else:
                    if len(split) != self.numfields:
                        err('inconsistent number of fields in headers')
                self.headers[restheaders[-1]] = split
                del restheaders[-1]
                continue

            if fmt.fields != 'auto':
                flds = [x.strip() for x in fmt.fields.split(',')]
                if self.numfields and len(flds) != self.numfields:
                    err('inconsistent number of fields in headers and '
                        'fields property')
                self.headers['names'] = flds

            if 'names' not in self.headers:
                err('no field names given and none found')
            names = self.headers['names']

            if fmt.end != 'auto' and fmt.end in line:
                break

            try:
                record = map(float, splitline(line))
            except Exception, exc:
                if fmt.end == 'auto':
                    break
                err('error splitting fields:\n%s' % fmt_ex(exc))
            if not self.numfields:
                self.numfields = len(record)
            elif len(record) != self.numfields:
                warn('inconsistent number of fields, ignoring record')
                continue
            self.data.append(record)
        self.numrecords = len(self.data)

        if skipping:
            warn('skipped whole file, wrong skip_until string?')
        return self


    def write(self, fmt, destination, warnfunc=None):
        """
        Write the data contained in self to file object `destination`, using
        output format `fmt`. Use `warnfunc` to emit warnings.
        """

        def warn(msg):
            if warnfunc:
                warnfunc('%s: while writing: %s' % (self.sourcename, msg))
        def err(msg):
            raise WriteError('%s: while writing: %s' % (self.sourcename, msg))

        # Name the input fields
        names = self.headers['names']
        if fmt.fieldnames:
            if len(fmt.fieldnames) != self.numfields:
                err('fieldnames property has %d fields, but input has %d' %
                    (len(fmt.fieldnames), self.numfields))
            names = fmt.fieldnames
        else:
            names = self.headers['names']

        records = [Record(zip(names, fields)) for fields in self.data]

        # This dict will hold all "global" names
        commoncontext = {}

        # First, import all modules
        for modname in fmt.module:
            try:
                mod = __import__(modname, None, None, ['dummy'])
            except Exception, exc:
                warn('could not import module %s:\n%s' % (modname, fmt_ex(exc)))
            else:
                for key in dir(mod):
                    if not key.startswith('_'):
                        commoncontext[key] = getattr(mod, key)

        # Some general items, useful for const calculations
        commoncontext.update({'records': records,
                              'numrecords': self.numrecords,
                              'numfields': self.numfields,
                              'fieldnames': self.headers['names'],
                              'headers': self.headers,
                              'skipped': self.skipped,
                              'defs': Namespace(self.defs),
                              })

        # Now, execute all const statements
        for constex in fmt.const:
            try:
                local = {}
                exec constex in commoncontext, local
            except Exception, exc:
                err('error executing const statement %r:\n%s' %
                    (constex, fmt_ex(exc)))
            else:
                commoncontext.update(local)

        # Do all assertions
        cont = 0
        for assex in fmt.assertion:
            try:
                result = eval(assex, commoncontext)
            except Exception, exc:
                warn('error evaling assertion %r (ignored):\n%s' %
                     (assex, fmt_ex(exc)))
                result = True
            if not result:
                err('assertion %r failed' % assex)

        # Determine the output fields
        if not fmt.outfields:
            err('no output fields defined')
        outfields = []
        for fields in fmt.outfields:
            if fields.startswith('!'):
                try:
                    fnames = eval(fields[1:], commoncontext)
                except Exception, exc:
                    err('error evaling outfields expression %r:\n%s' %
                        (fields[1:], fmt_ex(exc)))
            else:
                fnames = [name.strip() for name in fields.split(',')]
            outfields.extend(fnames)

        # Writing starts here...

        # First, the prologue
        if fmt.prologue:
            prologue = Template('\n'.join(fmt.prologue))
            destination.write(
                prologue.safe_substitute(commoncontext) + '\n')

        # Write headers if requested
        if fmt.headers:
            destination.write(fmt.fieldsep.join(outfields))

        # Then, all records -- record the number of records actually written
        # to be able to give a warning if none are
        c = 0
        for i, r in enumerate(records):
            reccontext = {}
            for name, value in r.pairs:
                reccontext[name] = value
            reccontext['i'] = i
            reccontext['r'] = r

            context = commoncontext.copy()
            context.update(reccontext)

            cont = 0
            for condex in fmt.condition:
                try:
                    result = eval(condex, context)
                except Exception, exc:
                    warn('error evaling condition %r (condition ignored):\n%s' %
                         (condex, fmt_ex(exc)))
                    # In dubio pro reo...
                    result = True
                if not result:
                    cont = 1
                    break
            if cont:
                continue
            c += 1

            for fieldex in fmt.field:
                try:
                    exec fieldex in context
                except Exception, exc:
                    err('error executing field statement %r:\n%s' %
                        (fieldex, fmt_ex(exc)))

            try:
                destination.write(fmt.fieldsep.join(
                    str(context[name]) for name in outfields))
            except KeyError, exc:
                err('output field %s not in context' % exc.args[0])
            destination.write('\n')

        if c == 0:
            warn('no records were written at all, check the conditions')

        # Finally, the epilogue
        if fmt.epilogue:
            epilogue = Template('\n'.join(fmt.epilogue))
            destination.write(
                epilogue.safe_substitute(commoncontext) + '\n')
