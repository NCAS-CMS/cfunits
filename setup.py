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
                yield filename.replace('cf/', '', 1)

# Check that the dependencies are met
for _module in ('netCDF4', 'numpy'):
    try:
        imp.find_module(_module)
    except ImportError as error:
        raise ImportError("Missing dependency. cf requires package %s. %s" %
                          (_module, error))
#--- End: for
       
version      = '1.0b1'
packages     = ['cfunits']
etc_files    = [f for f in find_package_data_files('cfunits/etc')]

package_data = etc_files

with open('README.md') as ldfile:
    long_description = ldfile.read()

setup(name = "cf",
      long_description = long_description,
      version      = version,
      description  = "A python interface to UNIDATA's Udunits-2 package with CF extensions ",
      author       = "David Hassell",
      author_email = "d.c.hassell at reading.ac.uk",
      url          = "http://cfpython.bitbucket.org/",
      download_url = "https://bitbucket.org/cfpython/cf-python/downloads",
      platforms    = ["Linux", "MacOS"],
      license      = ["OSI Approved"],
      keywords     = ['cf', 'udunits', 'numpy','netcdf','data','science','network','oceanography','meteorology','climate'],
      classifiers  = ["Development Status :: 3 - Alpha",
                      "Intended Audience :: Science/Research", 
                      "License :: OSI Approved", 
                      "Topic :: Software Development :: Libraries :: Python Modules",
                      "Topic :: System :: Archiving :: Compression",
                      "Operating System :: OS Independent"],
      packages     = ['cfunits'],
      package_data = {'cfunits': package_data},
      scripts      = ['scripts/cfa',
                      'scripts/cfdump'],
      requires     = ['netCDF4 (>=0.9.7)',
                      'numpy (>=1.7)',                      
                      ],
  )
