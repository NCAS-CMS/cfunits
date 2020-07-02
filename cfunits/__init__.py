'''A python interface to UNIDATA's UDUNITS-2 package with CF extensions

Store, combine and compare physical units and convert numeric values
to different units.

Units are as defined in UNIDATA's UDUNITS-2 package , except for
reference time units (such as 'days since 2000-12-1' in the
'proleptic_gregorian' calendar), which are handled by the `cftime`
python package.

In addition, some units are either new to, modified from, or removed
from the standard UDUNITS-2 database in order to be more consistent
with the CF conventions.


'''

__Conventions__  = 'CF-1.8'
__author__       = 'David Hassell'
__author__     = 'David Hassell'
__date__       = '2020-07-02'
__version__    = '3.2.8'
__cf_version__ = '1.8'

from distutils.version import LooseVersion
import platform

try:
    import cftime
except ImportError as error1:
    raise ImportError(error1)

# Check the version of python
_minimum_vn = '3.5'
if LooseVersion(platform.python_version()) < LooseVersion(_minimum_vn):
    raise RuntimeError(
        "Bad python version: cfunits requires python version {} or later. "
        "Got {}".format(
            _minimum_vn, platform.python_version()))

# Check the version of cftime
_minimum_vn = '1.1.3'
if LooseVersion(cftime.__version__) < LooseVersion(_minimum_vn):
    raise ValueError(
        "Bad cftime version: cfunits requires cftime>={}. Got {} at {}".format(
            _minimum_vn, cftime.__version__, cftime.__file__))

from .units import Units

