cfunits
=======

A Python interface to
[UNIDATA's UDUNITS-2 package](http://www.unidata.ucar.edu/software/udunits)
with CF extensions.

[![GitHub tag (latest by date)](https://img.shields.io/github/v/tag/NCAS-CMS/cfunits?color=000000&label=latest%20version)](https://ncas-cms.github.io/cfunits/Changelog.html)
[![PyPI](https://img.shields.io/pypi/v/cfunits?color=000000)](https://pypi.org/project/cfunits/)
[![Conda](https://img.shields.io/conda/v/ncas/cfunits?color=000000)](https://ncas-cms.github.io/cfunits/installation.html#conda)

[![Conda](https://img.shields.io/conda/pn/ncas/cfunits?color=2d8659)](https://ncas-cms.github.io/cfunits/installation.html#operating-systems) [![Website](https://img.shields.io/website?color=2d8659&down_message=online&label=documentation&up_message=online&url=https%3A%2F%2Fncas-cms.github.io%2Fcfunits%2F)](https://ncas-cms.github.io/cfunits/index.html) [![GitHub](https://img.shields.io/github/license/NCAS-CMS/cfunits?color=2d8659)](https://github.com/NCAS-CMS/cfunits/blob/master/LICENSE)

[![GitHub Workflow Status](https://img.shields.io/github/workflow/status/NCAS-CMS/cfunits/Run%20test%20suite?color=006666&label=test%20suite%20workflow)](https://github.com/NCAS-CMS/cfunits/actions) [![Codecov](https://img.shields.io/codecov/c/github/NCAS-CMS/cfunits?color=006666)](https://codecov.io/gh/NCAS-CMS/cfunits)

Store, combine and compare physical units and convert numeric values
to different units.

Units are as defined in UNIDATA's UDUNITS-2 package, except for
reference time units (such as 'days since 2000-12-1' in the
'proleptic_gregorian' calendar), which are handled by the
[`cftime` Python package](https://unidata.github.io/cftime).

In addition, some units are either new to, modified from, or removed
from the standard UDUNITS-2 database in order to be more consistent
with the [CF conventions](http://cfconventions.org/).

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
