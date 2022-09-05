"""A Python interface to UNIDATA's UDUNITS-2 package with CF extensions.

Store, combine and compare physical units and convert numeric values
to different units.

Units are as defined in UNIDATA's UDUNITS-2 package , except for
reference time units (such as 'days since 2000-12-1' in the
'proleptic_gregorian' calendar), which are handled by the `cftime`
Python package.

In addition, some units are either new to, modified from, or removed
from the standard UDUNITS-2 database in order to be more consistent
with the CF conventions.

"""

__Conventions__ = "CF-1.8"
__date__ = "2021-08-09"
__version__ = "3.3.4"
__cf_version__ = "1.8"

import platform as _platform
import sys as _sys
from pkg_resources import parse_version as _parse_version

try:
    import cftime
except ImportError as error1:
    raise ImportError(error1)

if _sys.version_info < (3, 6):
    raise RuntimeError(
        f"Bad Python version: cfunits requires Python version {_minimum_vn} "
        f"or later. Got {_platform.python_version()}"
    )

# Check the version of cftime
_minimum_vn = "1.5.0"
if _parse_version(cftime.__version__) < _parse_version(_minimum_vn):
    raise ValueError(
        f"Bad cftime version: cfunits requires cftime>={_minimum_vn}. Got "
        f"{cftime.__version__} at {cftime.__file__}"
    )

from .units import Units  # noqa: F401
