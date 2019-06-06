.. currentmodule:: cfunits
.. default-role:: obj

.. _Installation:

**Installation**
================

----

Version |release|

.. _Python-versions:

**Python versions**
-------------------

As of version 3.0.0, cfunits works for Python 3 only.

(Version 1.9 of cfunits works for Python 2 and Python 3.)

.. _pip:
  
**pip**
-------

----

To install cfunits and *most* of its :ref:`dependencies
<Dependencies>` (i.e. all except the UDUNITS library) run, for
example:

.. code-block:: shell
   :caption: *Install as root, with any missing dependencies.*
	     
   pip install cfunits

.. code-block:: shell
   :caption: *Install as a user, with any missing dependencies.*
	     
   pip install cfunits --user

To install cfunits without any of its dependencies then run, for example:

.. code-block:: shell
   :caption: *Install as root without installing any of the
             dependencies.*
	     
   pip install cfunits --no-deps

See the `documentation for pip install
<https://pip.pypa.io/en/stable/reference/pip_install/>`_ for further
options.

.. _Source:

**Source**
----------

----

To install from source:

1. Download the cfunits package from https://pypi.org/project/cfunits

2. Unpack the library (replacing ``<version>`` with the version that
   you want to install, e.g. ``3.0.0``):

   .. code:: bash
	 
      tar zxvf cfunits-<version>.tar.gz
      cd cfunits-<version>

3. Install the package:
  
  * To install the cfunits package to a central location:

    .. code:: bash
	 
       python setup.py install

  * To install the cfunits package locally to the user in the default
    location:

    .. code:: bash

       python setup.py install --user

  * To install the cfunits package in the <directory> of your choice:

    .. code:: bash

       python setup.py install --home=<directory>

.. _Tests:

**Tests**
---------

----

Tests are run from within the ``cfunits/test`` directory:

.. code:: bash
 
   python run_tests.py
       
.. _Dependencies:

**Dependencies**
----------------

----

The cfunits package requires:

* `Python <https://www.python.org/>`_, version  3 or newer,

* `numpy <http://www.numpy.org/>`_, version 1.15 or newer,

* `cftime <https://pypi.org/project/cftime/>`_, version 1.0.0
  or newer, and

* The `UNIDATA UDUNITS library
  <http://www.unidata.ucar.edu/software/udunits>`_, version 2 or
  newer. This is a C library which provides support for units of
  physical quantities.

  If the UDUNITS2 shared library file (`libudunits2.so.0` on GNU/Linux
  or `libudunits2.0.dylibfile` on Mac OS) is in a non-standard
  location then its path should be added to the `LD_LIBRARY_PATH`
  environment variable. It may also be necessary to specify the
  location of the `udunits2.xml` file in the `UDUNITS2_XML_PATH`
  environment variable (although the default location is usually
  correct).

  UDUNITS is available via Anaconda with:

  .. code:: bash

     conda install -c conda-forge udunits2=2.2.20

.. _Code-repository:

**Code repository**
-------------------

----

The complete source code is available at https://github.com/NCAS-CMS/cfunits

