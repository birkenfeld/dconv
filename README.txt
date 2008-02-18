d2d data file conversion utility
================================

:Author: Georg Brandl
:Last updated: Feb 8, 2008

This utility converts data files between different (ASCII) formats.
Input and output formats are described using a simple "format
description" language.


Format descriptions
-------------------

A format description is a block of text that consists of simple
one-line property-value assignments.  Every line is either empty, a
comment (starts with `#`) or a property assignment of the form
`property: value`.

String properties can be given with or without quotes; if quoted, they
are evaluated as a Python string (enabling you to use escape
sequences).

Some properties can be given multiple times; this is noted in their
description.

Input format
~~~~~~~~~~~~

Input data files consist of three parts (where the first two are
optional):

* Skipped text (which can contain global definitions)
* Headers (descriptions etc. for every field)
* Data, organized as one record per line

The input format description can have these properties:

`comments` : `none`, or a string (default: `none`)

    If this is not `none`, lines in the data file starting with the
    given string are ignored.  Blank lines are always ignored.

`defs` :  `auto`, `equals`, `colon` or `none` (default: `auto`)

    If `none`, no definitions are recognized in skipped text.  If
    `equals`, definitions of the form `name = value` are recognized, if
    `colon`, definitions of the form `name: value` are recognized. The
    value `auto` allows both forms of definitions.

    For definition values that are of the form ``number unit``, the
    unit is split off and only the number is kept converted to a float.

`skip_until` : a string (no default)

    If this property is given, all lines at the beginning of the file
    are skipped, until a line contains this string.  (The line
    containing the string is not skipped; use `extra_skip` to do that.)

`extra_skip` : an integer (default: 0)

    This amount of lines is skipped at the beginning of the file, or
    after the `skip_until` string has been found.

`headers` : [multiple] a string (no default)

    This option marks the first line (or subsequent lines, if given
    multiple times) of the data to be headers.  The headers are read,
    split and stored in the `headers` attribute of the Data instance,
    with the given value as the key.  The headers with the key `name`
    are special: they are used for assigning names to the record
    fields.

`fields` : a comma-separated list of strings (no default)

    If the record field names are not in the data file, or the ones
    provided in the data file are not usable, this property can be used
    to assign names to the record fields.  (It has priority over a
    `names` header, if given.)

`fieldsep` : a string (default: `" \t"`)

    Record lines are split at the delimiters given (each character is a
    separate delimiter).

`linejunk` : [multiple] a string (no default)

    The given strings are ignored when splitting a record line.

`fieldregex` : a string (compilable as a regular expression) (no default)

    If this is given, the `fieldsep` and `linejunk` properties are
    ignored, and instead each line containing fields is matched against
    the regular expression, each subgroup of the regex being regarded
    as one field.

`end` : `auto`, or a string (default: `auto`)

    If this is `auto`, reading the data stops as soon as an error is
    encountered.

    Else, reading the data stops as soon as a line contains the given
    string.


Output format
~~~~~~~~~~~~~

`fieldnames` : a comma-separated list of strings

    This list renames the fields coming from the input file to the
    given names.

`module` : [multiple] a module name

    All modules given are imported and their contents can be used in
    the code calculating constants, conditions and fields.

`assertion` : [multiple] a Python expression

    The given expressions are evaluated once, before writing individual
    records.  If one expression is evaluated to a False value, writing
    stops with an error.  This can be used to make sure the data is in
    the correct format.

`const` : [multiple] a Python statement

    The given statements are executed before individual records are
    converted.  This can be used to set constants for calculation; they
    are available in `condition` and `field` expressions.

`condition` : [multiple] a Python expression

    The given conditions are tested for each record before it is
    written.  If any condition is evaluated to a False value, the
    record is skipped.

`field` : [multiple] a Python statement

    These statements are executed once for each record, in the order
    they occur in the definition.  They can be used to calculate output
    fields.

`outfields` : [multiple] a string

    This property selects which fields are written as the output
    record.  The field names available are names created by `field`
    statements and the field names of the input file (possibly renamed
    by a `fieldnames` property).

    The value must be either a comma-separated list of strings, or a
    `!` followed by a Python expression.  If it's a list of strings,
    they will be taken directly as names.  If it's an expression, it
    must evaluate to a list of strings.  All the named fields are then
    added as output fields.

`headers` : True/False (default: False)

    If true, write the output field names as the first line in the
    output file.

`fieldsep` : a string

    This string is used to separate output fields.

`prologue` : [multiple] a string

    All strings given here are written to the output file before any
    data record, one string per line.

    Within the strings, you can use variable substitution of the form
    `$name` or `${name}` to insert constants into the text.

`epilogue` : [multiple] a string

    All strings given here are written to the output file after all
    data records, one string per line.  You can use the same
    substitution mechanism as for `prologue`.


Additional variables available for code execution
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

When executing code for `const`, `condition` and `field` items, or
substituting names in `prologue` and `epilogue`, these names are
always defined:

* `records` -- a list of all records in the input data
* `numrecords` -- the total number of records
* `numfields` -- the number of fields in a record
* `fieldnames` -- a list of `numfields` field names from the input file
  (*not* influenced by a `fieldnames` property)
* `headers` -- the dictionary of headers
* `skipped` -- a list of all skipped lines from the input file
* `defs` -- an object that has all definitions from the input file as
  attributes

* and of course, all Python built-in functions.

These names are additionally defined for `condition` and `field` item code:

* `i` -- sequential number of the current record, starting with 0
* `r` -- current record, you can access the fields as attributes
