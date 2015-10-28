Introduction
============

<<<<<<< HEAD
A python interface to `UNIDATA's Udunits-2 package
=======
A python interface to `UNIDATA's Udunits-2 library
>>>>>>> 8503d21b6cd26cba5193e8294b8f329650181cd0
<http://www.unidata.ucar.edu/software/udunits>`_ with CF extensions

Store, combine and compare physical units and convert numeric values to different units.

<<<<<<< HEAD
Units are as defined in UNIDATA's Udunits-2 package , except for
=======
Units are as defined in UNIDATA's Udunits-2 library, except for
>>>>>>> 8503d21b6cd26cba5193e8294b8f329650181cd0
reference time units (such as ``'days since 2000-12-1'`` in the
``'proleptic_gregorian'`` calendar), which are handled by the `netCDF4
python package <https://pypi.python.org/pypi/netCDF4>`_.

In addition, some units are either new to, modified from, or removed
from the standard Udunits-2 database in order to be more consistent
with the `CF conventions <http://cfconventions.org/>`_.
