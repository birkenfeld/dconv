"""
    dconv.outformats
    ~~~~~~~~~~~~~~~~

    :author: Georg Brandl
    :license: GPL
"""

parratt = """
# Output format suitable for Parratt and MotoFit
# Expects input file with om, Detector, and Monitor1 fields

module: math

def: cutoff = -1

const: qvalue = lambda om: 4*pi/defs.l * sin(-om * pi/180)
const: norm = max(r.Detector/r.Monitor1 for r in records if r.Monitor1 and qvalue(r.om) > defs.cutoff)

condition: Monitor1 > 0
condition: qvalue(om) > defs.cutoff

field: R = (Detector / Monitor1) / norm
field: q = qvalue(om)
field: Rerror = 0

outfields: q, R, Rerror
fieldsep: '\t'

filename_ext: dat
"""

motofit = parratt

_simulreflec = """
# Output format suitable for SimulReflec
# Expects input file with om, Detector, and Monitor1 fields

const: comment = skipped[-1]
const: countmax = max(r.Detector/r.Monitor1 for r in records if r.Monitor1)

condition: Monitor1 > 0

field: norm = Detector / Monitor1
field: R = norm / countmax
field: Rerror = 0

outfields: om, R, Rerror
fieldsep: '\t'
"""

simulreflec_nonpol = _simulreflec + """
prologue: # Comment = $comment
prologue: # Particles = neutrons
prologue: # Polarisation = non polarised
prologue: # AbscissesUnits = deg
prologue: # TimeOfFlight = False
"""

simulreflec_pol = _simulreflec + """
prologue: # Comment = $comment
prologue: # Particles = neutrons
prologue: # Polarisation = polarised
prologue: # AbscissesUnits = deg
prologue: # TimeOfFlight = False

# XXX add more fields for polarised neutrons
"""

simple_norm = """
# Output format for generic data
# Expects input file with at least Detector, Timer1 and Monitor1 fields
# Calculates a normalized count rate

condition: Monitor1 > 0

field: norm = (Detector / Monitor1) / Timer1

outfields: !fieldnames[:-3]
outfields: norm
fieldsep: '\t'
"""
