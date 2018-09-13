Version 1.8 (13 September 2018)
-------------------------------

* Trap "ValueError: negative reference year in time units, must be
  >= 1" so that a Units object is returned that has isvalid=False.

* Added "message" attribute that reports on why bad units are
  bad. Is "None" if units are OK.
	
Version 1.7 (23 August 2018)
----------------------------

* Python 3 compatibility (with many thanks to Eric Hutton)

Version 1.6 (23 August 2018)
----------------------------

* Bad units now do not raise an exception, but may be checked with
  the "isvalid" atttribute.	

Version 1.5 (24 February 2017)
------------------------------

* Removed explicit dependency checks

* brough in line with cf-python v1.5
	
Version 1.1.4 (17 February 2016)
--------------------------------

* Bug fix to setup.py
	
Version 1.1 (28 October 2015)
-----------------------------

* Bug fix to Units.conform for scalar numpy arrays.

* Removed support for netCDF4-python versions < 1.1.1

* Same as cf/units.py in cf-python version 1.1

Version 1.0 (27 May 2015)
-------------------------

* Initial release

* Same as cf/units.py in cf-python version 1.0
