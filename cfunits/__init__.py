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

import platform
from distutils.version import LooseVersion

try:
    import cftime
except ImportError as error1:
    raise ImportError(error1)

# Check the version of Python
_minimum_vn = "3.6.0"
if LooseVersion(platform.python_version()) < LooseVersion(_minimum_vn):
    raise RuntimeError(
        f"Bad Python version: cfunits requires Python version {_minimum_vn} "
        f"or later. Got {platform.python_version()}"
    )

# Check the version of cftime
_minimum_vn = "1.5.0"
if LooseVersion(cftime.__version__) < LooseVersion(_minimum_vn):
    raise ValueError(
        f"Bad cftime version: cfunits requires cftime>={_minimum_vn}. Got "
        f"{cftime.__version__} at {cftime.__file__}"
    )

from .units import Units  # noqa: F401
