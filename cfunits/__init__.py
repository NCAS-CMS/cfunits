'''

CF is a netCDF convention which is in wide and growing use for the
storage of model-generated and observational data relating to the
atmosphere, ocean and Earth system.

It has been agreed that the CF conventions should include an abstract
data model for data and metadata corresponding to the most up to date
standard, and such a model is has been proposed. This package is an
implementation of this CF data model, and as such it is an API allows
for the full scope of data and metadata interactions described by the
CF conventions.

With this package you can:

    * Read CF-netCDF and PP format files

    * Aggregate collections of fields into as few multidimensional
      fields as possible.

    * Write fields to CF-netCDF files on disk.

    * Create, delete and modify a field's data and metadata.

    * Select fields according to their metadata.

    * Subspace a field's data to create a new field.

    * Perform broadcastable, metadata-aware arithmetic and comparison
      operations with fields.

    * Collapse fields.

All of the above use Large Amounts of Massive Arrays (LAMA)
functionality, which allows multiple fields larger than the available
memory to exist and be manipulated.

See the cf-python home page (http://code.google.com/p/cf-python) for
downloads, installation and source code.
'''

__Conventions__  = 'CF-1.5'
__author__       = 'David Hassell'
__date__         = '19 May 2015'
__version__      = '1.0b1'

import imp
import platform

# Check the version of python
if not '2.6.0' <= platform.python_version() < '3.0.0':
    raise RuntimeError(
        "Bad python version: cf requires 2.6 <= python < 3.0. Got %s" %
        platform.python_version())

# Check the version of numpy
import numpy
if numpy.__version__ < '1.7':
    raise ImportError(
        "Bad numpy version: cf %s requires numpy >= 1.7. Got %s" %
        (__version__, numpy.__version__))

# Check the version of netCDF4
import netCDF4
if netCDF4.__version__ < '0.9.7':
    raise ImportError(
        "Bad netCDF4 version: cf %s requires netCDF4 >= 0.9.7. Got %s" %
        (__version__, netCDF4.__version__))

from .units import Units

