# -*- coding: utf-8 -*-

#
# omdict - Ordered Multivalue Dictionary.
#
# Ansgar Grunseid
# grunseid.com
# grunseid@gmail.com
#
# License: Build Amazing Things (Unlicense)
#

import sys
from os.path import dirname, join as pjoin

# There's no typing module until 3.5
if sys.version_info >= (3, 5):
    from typing import Dict

from .orderedmultidict import *  # noqa

# Import all variables in __version__.py without explicit imports.
meta = {}  # type: Dict
with open(pjoin(dirname(__file__), '__version__.py')) as f:
    exec(f.read(), meta)
globals().update(dict((k, v) for k, v in meta.items() if k not in globals()))
