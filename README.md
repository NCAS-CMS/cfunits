cfunits
=======

A python interface to UNIDATA's UDUNITS-2 package with CF extensions.

Store, combine and compare physical units and convert numeric values
to different units.

Units are as defined in UNIDATA's UDUNITS-2 package , except for
reference time units (such as 'days since 2000-12-1' in the
'proleptic_gregorian' calendar), which are handled by the `cftime`
python package.

In addition, some units are either new to, modified from, or removed
from the standard UDUNITS-2 database in order to be more consistent
with the CF conventions.

Documentation
=============

http://ncas-cms.github.io/cfunits


Installation
============

https://ncas-cms.github.io/cfunits/installation.html

Tests
=====

The test script is in the ``cfunits/test`` directory:

    python test/run_tests.py


