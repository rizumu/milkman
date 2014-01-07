# -*- coding: utf-8 -*-
"""
pyrax._compat
~~~~~~~~~~~~~~

Some py2/py3 compatibility support based on a stripped down
version of six so we don't have to depend on a specific version
of it.

:copyright: Copyright 2013 by the Jinja team, see AUTHORS.
:license: BSD, see LICENSE for details.
"""
import sys

PY2 = sys.version_info[0] == 2


if not PY2:
    text_type = str
    iteritems = lambda d: iter(d.items())
    get_next = lambda x: x.__next__

else:
    text_type = unicode
    iteritems = lambda d: d.iteritems()
    get_next = lambda x: x.next
