# Documentation

http://ncas-cms.github.io/cfunits


# Dependencies

* The package runs on [**Linux**](http://en.wikipedia.org/wiki/Linux)
  and [**Mac OS**](http://en.wikipedia.org/wiki/Mac_OS) operating
  systems.

* Requires a [**python**](http://www.python.org) version 3 or newer.
 
* Requires the [**python numpy
  package**](https://pypi.python.org/pypi/numpy) at version 1.15 or
  newer.

* Requires the [**python cftime
  package**](https://pypi.python.org/pypi/cftime) at version 1.0.0 or
  newer.

* Requires the [**UNIDATA Udunits-2
  library**](http://www.unidata.ucar.edu/software/udunits). This is a
  C library which provides support for units of physical
  quantities. If The Udunits-2 shared library file
  (``libudunits2.so.0`` on Linux or ``libudunits2.0.dylibfile`` on Mac
  OS) is in a non-standard location then its path should be added to
  the ``LD_LIBRARY_PATH`` environment variable.

# Installation

To install from [**PyPI**](https://pypi.python.org/pypi/cfunits):

    pip install cfunits

Alternatively, to install from source:

1. Download the cfunits package from https://pypi.org/project/cfunits

2. Unpack the library (replacing ``<version>`` with the version that
   you want to install, e.g. ``3.2.2``):

      tar zxvf cfunits-<version>.tar.gz
      cd cfunits-<version>

3. Install the package:
  
  * To install the cf-python package to a central location:

       python setup.py install

  * To install the cf-python package locally to the user in the default
    location:

       python setup.py install --user

  * To install the cf-python package in the <directory> of your choice:

       python setup.py install --home=<directory>

# Tests

The test script is in the ``test`` directory:

    python test/run_tests.py


