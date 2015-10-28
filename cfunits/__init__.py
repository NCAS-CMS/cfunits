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

__Conventions__  = 'CF-1.5'
__author__       = 'David Hassell'
__date__         = '28 October 2015'
__version__      = '1.1'

from distutils.version import StrictVersion
import imp
import platform

if not (StrictVersion('2.6.0')
        <= StrictVersion(platform.python_version())
        < StrictVersion('3.0.0')):
    raise ValueError(
        "Bad python version: cf requires 2.6 <= python < 3.0. Got %s" %
        platform.python_version())

# Check the version of numpy
import numpy
if StrictVersion(numpy.__version__) < StrictVersion('1.7'):
    raise ImportError(
        "Bad numpy version: cf %s requires numpy >= 1.7. Got %s" %
        (__version__, numpy.__version__))

# Check the version of netCDF4
import netCDF4
if StrictVersion(netCDF4.__version__) < StrictVersion('0.9.7'):
    raise ImportError(
        "Bad netCDF4 version: cf %s requires netCDF4 >= 0.9.7. Got %s" %
        (__version__, netCDF4.__version__))

from .units import Units

