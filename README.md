Home page
=========

* [**cfunits-python**](https://bitbucket.org/cfpython/cfunits-python "cfunits-python home page")

----------------------------------------------------------------------

Documentation
=============

* [**Online documentation for the latest stable
  release**](http://pythonhosted.org/cfunits "cfunits documentation")

* Offline HTML documention for the installed version may be found by
  pointing a browser to ``docs/build/index.html``.


----------------------------------------------------------------------

Dependencies
============

* The package runs on [**Linux**](http://en.wikipedia.org/wiki/Linux)
  and [**Mac OS**](http://en.wikipedia.org/wiki/Mac_OS) operating
  systems.

* Requires a [**python**](http://www.python.org) version from 2.6 up
  to, but not including, 3.0.
 
* Requires the [**python numpy
  package**](https://pypi.python.org/pypi/numpy) at version 1.7 or
  newer.

* Requires the [**python netCDF4
  package**](https://pypi.python.org/pypi/netCDF4) at version 1.1.1 or
  newer, *but not version 1.2*. This package requires the
  [**netCDF**](http://www.unidata.ucar.edu/software/netcdf),
  [**HDF5**](http://www.hdfgroup.org/HDF5) and
  [**zlib**](ftp://ftp.unidata.ucar.edu/pub/netcdf/netcdf-4)
  libraries.

* Requires the [**UNIDATA Udunits-2
  library**](http://www.unidata.ucar.edu/software/udunits). This is a
  C library which provides support for units of physical
  quantities. If The Udunits-2 shared library file
  (``libudunits2.so.0`` on Linux or ``libudunits2.0.dylibfile`` on Mac
  OS) is in a non-standard location then its path should be added to
  the ``LD_LIBRARY_PATH`` environment variable.

----------------------------------------------------------------------

Installation
============

To install from [**PyPI**](https://pypi.python.org/pypi/cfunits):

    pip install cfunits

Alternatively, to install from source:

To install from [**PyPI**](https://pypi.python.org/pypi/cfunits):

    pip install cfunits

Alternatively, to install from source:

1.  Download the cfunits package from [**cfunits-python
    downloads**](https://bitbucket.org/cfpython/cfunits-python/downloads).
   
2.  Unpack the library:
   
        tar zxvf cfunits-1.1.tar.gz
        cd cfunits-1.1
	  
3.   Install the package:
   
    *  To install to a central location:
     
            python setup.py install
       
    * To install locally to the user in a default location:
       
            python setup.py install --user
       
    *  To install to the <directory> of your choice:
       
            python setup.py install --home=<directory>

----------------------------------------------------------------------

Tests
=====

The test script is in the ``test`` directory:

    python test/run_tests.py


----------------------------------------------------------------------

Code license
============

[**MIT License**](http://opensource.org/licenses/mit-license.php)

  * Permission is hereby granted, free of charge, to any person
    obtaining a copy of this software and associated documentation
    files (the "Software"), to deal in the Software without
    restriction, including without limitation the rights to use, copy,
    modify, merge, publish, distribute, sublicense, and/or sell copies
    of the Software, and to permit persons to whom the Software is
    furnished to do so, subject to the following conditions:

  * The above copyright notice and this permission notice shall be
    included in all copies or substantial portions of the Software.

  * THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
    EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
    MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
    NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT
    HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY,
    WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
    OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
    DEALINGS IN THE SOFTWARE.
