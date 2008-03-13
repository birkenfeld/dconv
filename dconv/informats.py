"""
    dconv.informats
    ~~~~~~~~~~~~~~~

    :author: Georg Brandl
    :license: GPL
"""

mira = """
defs: auto
skip_until: "scan data:"
extra_skip: 2
headers: names
headers: units
end: auto
comments: none
linejunk: ";"
"""

treff = """
defs: none
extra_skip: 5
end: auto
comments: none
fields: phi, om, _, Detector, _, Monitor1, _, _, _, _, Timer1
"""
