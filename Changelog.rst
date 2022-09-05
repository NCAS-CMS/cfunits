version 3.3.5
-------------
----

**xxxx-xx-xx**

* Remove calls to ``LooseVersion`` from ``distutils`` due to deprecation of that package,
  replaced with ``pkg_resources.parse_version``.

version 3.3.4
-------------
----

**2021-08-09**

* Now supports the Windows operating system
  (https://github.com/NCAS-CMS/cfunits/issues/31)

version 3.3.3
-------------
----

**2021-05-24**

* Fixed error in `setup.py` that prevented installation via `pip`.

version 3.3.2
-------------
----

**2021-05-21**

* Refactor to remove the dependency on `cftime.utime`, that was removed
  at `cftime` version 1.5.0
  (https://github.com/NCAS-CMS/cfunits/issues/25)
* Changed dependency: ``cftime>=1.5.0``

version 3.3.1
-------------
----

**2020-11-27**

* Make invalid units non-equivalent and non-equal
  (https://github.com/NCAS-CMS/cfunits/issues/19)

version 3.3.0
-------------
----

**2020-10-09**

* Python 3.5 support deprecated (3.5 was retired on 2020-09-13)
* Make ``Units('')`` and ``Units()`` equivalent (but still not equal).

version 3.2.9
-------------
----

**2020-07-24**

* New attribute: `cfunits.Units.has_offset`
* `cftime.Units.reftime` now always returns a `cftime.datetime`
  object.
* Fixed bug that caused failure when hashing reference time units.
* Changed dependency: ``cftime>=1.2.1``

version 3.2.8
-------------
----

**2020-07-02**

* Fixed bug that caused failure when an `int` or `float` was input to
  `cfunits.Units.conform`
  (https://github.com/NCAS-CMS/cfunits/issues/9).
* Allowed `list` and `tuple` to be input to `cfunits.Units.conform`
  (https://github.com/NCAS-CMS/cfunits/issues/9).

version 3.2.7
-------------
----

**2020-05-20**

* Minor changes to allow for ``cftime==1.1.3``
* Changed dependency: ``cftime>=1.1.3``

version 3.2.6
-------------
----

**2020-04-27**

* Fixed bug that caused a `KeyError: '1r'` exception, due to an
  incorrect format statement.

version 3.2.5
-------------
----

**2020-03-26**

* Check that the udunits2 library exists (with thanks to Gareth
  Jones).
* Changed dependency: ``cftime>=1.1.1``

version 3.2.4
-------------
----

**2020-01-07**

* Use ctypes.util.find_library to get name of udunits2 library (with
  thanks to Lance Helsten)

version 3.2.3
-------------
----

**2019-11-28**

* Fixed a bug that raised an exception for units specified by
  non-strings (https://github.com/NCAS-CMS/cfunits/issues/1).

version 3.2.2
-------------
----

**2019-09-16**

* Added `_units_since_reftime` attribute.

version 3.2.0
-------------
----

**2019-09-12**

* Added `_canonical_calendar` attribute.
* Improved testing in `Unit.equivalent`.

version 3.1.1
-------------
----

**2019-08-02**

* Incremented version.

version 3.1.0
-------------
----

**2019-08-02**

* Added `reason_notvalid` attribute, and improved handling of invalid
  calendars.

version 3.0.0
-------------
----

**2019-05-28**

* Python 2 support deprecated.

version 1.9
-----------
----

**2019-02-14**

* Updated documentation to mention the isvalid attribute.
	
version 1.8 
-----------
----

**2018-09-13**

* Trap "ValueError: negative reference year in time units, must be >=
  1" so that a Units object is returned that has isvalid=False.
* Added "message" attribute that reports on why bad units are bad. Is
  "None" if units are OK.
	
version 1.7 
-----------
----

**2018-08-23**

* Python 3 compatibility (with many thanks to Eric Hutton)

version 1.6 
-----------
----

**2018-08-23**

* Bad units now do not raise an exception, but may be checked with the
  "isvalid" attribute.

version 1.5 
-----------
----

**2017-02-24**

* Removed explicit dependency checks
* brought in line with cf-python v1.5
	
Version 1.1.4
-------------
----

**2016-02-17**

* Bug fix to setup.py
	
Version 1.1 
-----------
----

**2015-10-28**

* Bug fix to Units.conform for scalar numpy arrays.
* Removed support for netCDF4-python versions < 1.1.1
* Same as cf/units.py in cf-python version 1.1

version 1.0 
-----------
----

**2015-05-27**

* Initial release
* Same as cf/units.py in cf-python version 1.0
