.. currentmodule:: cfunits
.. default-role:: obj

.. _Installation:

**Installation**
================

----

Version |release| for CF-|version|

.. contents::
   :local:
   :backlinks: entry

.. _Operating-systems:

**Operating systems**
---------------------

The cfunits package works for Linux, Mac and Windows operating
systems.

----

.. _Python-versions:

**Python versions**
-------------------

cfunits works only with Python 3.6 or newer.

----

.. _pip:
  
**pip**
-------

To install cfunits and *most* of its :ref:`dependencies
<Dependencies>` (i.e. all except the UDUNITS library) run, for
example:

.. code-block:: console
   :caption: *Install as root, with any missing dependencies.*
	     
   $ pip install cfunits

.. code-block:: console
   :caption: *Upgrade as root, with any missing dependencies.*
	     
   $ pip install cfunits --upgrade

.. code-block:: console
   :caption: *Install as a user, with any missing dependencies.*
	     
   $ pip install cfunits --user

To install cfunits without any of its dependencies then run, for example:

.. code-block:: console
   :caption: *Install as root without installing any of the
             dependencies.*
	     
   $ pip install cfunits --no-deps

See the `documentation for pip install
<https://pip.pypa.io/en/stable/reference/pip_install/>`_ for further
options.

----

.. _Source:

**Source**
----------

To install from source:

1. Download the cfunits package from https://pypi.org/project/cfunits

2. Unpack the library (replacing ``<version>`` with the version that
   you want to install, e.g. ``3.3.4``):

   .. code:: console
	 
      $ tar zxvf cfunits-<version>.tar.gz
      $ cd cfunits-<version>

3. Install the package:
  
  * To install the cfunits package to a central location:

    .. code:: console
	 
       $ python setup.py install

  * To install the cfunits package locally to the user in the default
    location:

    .. code:: console

       $ python setup.py install --user

  * To install the cfunits package in the <directory> of your choice:

    .. code:: console

       $ python setup.py install --home=<directory>

----

.. _Tests:

**Tests**
---------

Tests are run from within the ``cfunits/test`` directory:

.. code:: console
 
   $ python run_tests.py
       
----

.. _Dependencies:

**Dependencies**
----------------

The cfunits package requires:

* `Python <https://www.python.org/>`_, version 3.6 or newer,

* `numpy <http://www.numpy.org/>`_, version 1.15 or newer,

* `cftime <https://pypi.org/project/cftime/>`_, version 1.5.0
  or newer, and

* `UNIDATA UDUNITS-2 library
  <http://www.unidata.ucar.edu/software/udunits>`_, version 2.2.25 or
  newer.

  UDUNITS-2 is a C library that provides support for units of physical
  quantities

  If the UDUNITS-2 shared library file (``libudunits2.so.0`` on
  GNU/Linux or ``libudunits2.0.dylibfile`` on MacOS) is in a
  non-standard location then its directory path should be added to the
  ``LD_LIBRARY_PATH`` environment variable. It may also be necessary
  to specify the location (directory path *and* file name) of the
  ``udunits2.xml`` file in the ``UDUNITS2_XML_PATH`` environment
  variable, although the default location is usually correct. For
  example, ``export
  UDUNITS2_XML_PATH=/home/user/anaconda3/share/udunits/udunits2.xml``.

  If you get an error that looks like ``assert(0 ==
  _ut_unmap_symbol_to_unit(_ut_system, _c_char_p(b'Sv'), _UT_ASCII))``
  then setting the ``UDUNITS2_XML_PATH`` environment variable is the
  likely solution.

  UDUNITS is available via conda with:

  .. code:: console

     $ conda install -c conda-forge udunits2>=2.2.25

* `packaging <https://pypi.org/project/packaging/>`_, version 20.0 or newer.

----


.. _Code-repository:

**Code repository**
-------------------

The complete source code is available at https://github.com/NCAS-CMS/cfunits
