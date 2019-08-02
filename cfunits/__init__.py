'''A python interface to UNIDATA's Udunits-2 package with CF extensions

Store, combine and compare physical units and convert numeric values
to different units.

Units are as defined in UNIDATA's Udunits-2 package , except for
reference time units (such as 'days since 2000-12-1' in the
'proleptic_gregorian' calendar), which are handled by the netCDF4
python package.

In addition, some units are either new to, modified from, or removed
from the standard Udunits-2 database in order to be more consistent
with the CF conventions.

See the cfunits-python home page
(https://bitbucket.org/cfpython/cfunits-python/) for downloads,
installation and source code.

'''

__Conventions__  = 'CF-1.7'
__author__       = 'David Hassell'
__date__         = '2019-08-02'
__version__      = '3.1.1'

from distutils.version import LooseVersion
import platform

# Check the version of python
minimum_vn = '3.0.0'
if LooseVersion(platform.python_version()) < LooseVersion(minimum_vn):
    raise ValueError(
        "Bad python version: cf requires python version {} or later. Got {}".format(
            minimum_vn,  platform.python_version()))

from .units import Units

