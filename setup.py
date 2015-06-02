from distutils.core import setup, Extension
from distutils.command.build import build
import os
import fnmatch
import sys
import imp
import subprocess

def find_package_data_files(directory):
    for root, dirs, files in os.walk(directory):
        for basename in files:
            if fnmatch.fnmatch(basename, '*'):
                filename = os.path.join(root, basename)
#                if filename.find('/.svn') > -1:
#                    continue
                yield filename.replace('cfunits/', '', 1)

# Check that the dependencies are met
for _module in ('netCDF4', 'numpy'):
    try:
        imp.find_module(_module)
    except ImportError as error:
        raise ImportError("Missing dependency. cfunits requires package %s. %s" %
                          (_module, error))
#--- End: for
       
version      = '1.0'
packages     = ['cfunits']
etc_files    = [f for f in find_package_data_files('cfunits/etc')]

package_data = etc_files

#with open('README.md') as ldfile:
#    long_description = ldfile.read()

long_description = '''A python interface to UNIDATA's Udunits-2 package with CF
extensions

Store, combine and compare physical units and convert numeric values
to different units.

Units are as defined in UNIDATA's Udunits-2 package , except for
reference time units (such as 'days since 2000-12-1' in the
'proleptic_gregorian' calendar), which are handled by the netCDF4
python package.

In addition, some units are either new to, modified from, or removed
from the standard Udunits-2 database in order to be more consistent
with the CF conventions.'''

# classifiers list at: https://pypi.python.org/pypi?%3Aaction=list_classifiers

setup(name = "cfunits",
      long_description = long_description,
      version      = version,
      description  = "A python interface to UNIDATA's Udunits-2 package with CF extensions ",
      author       = "David Hassell",
      author_email = "d.c.hassell at reading.ac.uk",
      url          = "https://bitbucket.org/cfpython/cfunits-python",
      download_url = "https://bitbucket.org/cfpython/cfunits-python/downloads",
      platforms    = ["Linux", "MacOS"],
      license      = ["MIT"],
      keywords     = ['cf', 'udunits','netcdf','data','science', 'oceanography', 'meteorology', 'climate'],
      classifiers  = ["Development Status :: 5 - Production/Stable",
                      "Intended Audience :: Science/Research", 
                      "License :: OSI Approved :: MIT License", 
                      "Topic :: Software Development :: Libraries :: Python Modules",
                      "Topic :: System :: Archiving :: Compression",
                      "Operating System :: MacOS",
                      "Operating System :: POSIX :: Linux",
                      "Programming Language :: Python :: 2.6",
                      "Programming Language :: Python :: 2.7",],
      packages     = ['cfunits'],
      package_data = {'cfunits': package_data},
      requires = ['netCDF4 (>=0.9.7)',
                  'numpy (>=1.7)',                      
              ],
  )
