.. currentmodule:: cfunits
.. default-role:: obj

**Introduction**
================

----

Version |release|

A Python interface to `UNIDATA's UDUNITS-2 library
<http://www.unidata.ucar.edu/software/udunits>`_ with CF extensions

Store, combine and compare physical units and convert numeric values to different units.

Units are as defined in UNIDATA's UDUNITS-2 library, except for
reference time units (such as ``'days since 2000-12-01'`` in the
``'proleptic_gregorian'`` calendar), which are handled by the `cftime
Python package <https://unidata.github.io/cftime>`_.

In addition, some units are either new to, modified from, or removed
from the standard UDUNITS-2 database in order to be more consistent
with the `CF conventions <http://cfconventions.org/>`_.
