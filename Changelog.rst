version 3.0.0
-------------
----

**2019-05-28**

* Python 2 deprecated.

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
  "isvalid" atttribute.

version 1.5 
-----------
----

**2017-02-24**

* Removed explicit dependency checks
* brough in line with cf-python v1.5
	
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
