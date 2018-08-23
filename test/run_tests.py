from __future__ import print_function

import unittest
import os
import sys

import netCDF4
import numpy
import datetime
import cfunits

from platform    import system, platform, python_version

# Build the test suite from the tests found in the test files.
testsuite = unittest.TestSuite()
testsuite.addTests(unittest.TestLoader().discover('test', pattern='test_*.py'))

# Run the test suite.
def run_test_suite(verbosity=2):
    runner = unittest.TextTestRunner(verbosity=verbosity)
    runner.run(testsuite)

if __name__ == '__main__':
    print('-------------------------')
    print('CFUNITS-PYTHON TEST SUITE')
    print('-------------------------')
    print('Run date:'              , datetime.datetime.now())
    print('Platform:'              , str(platform()))
    print('python:'                , str(python_version() + ' ' + str(sys.executable)))
    print('HDF5 lib version:'      , netCDF4. __hdf5libversion__)
    print('netcdf lib version:'    , netCDF4.__netcdf4libversion__)
    print('netcdf4-python version:', netCDF4.__version__)
    print('numpy version:'         , numpy.__version__)
    print('cfunits-python version:', cfunits.__version__)
    print('cfunits-python path:'   , os.path.abspath(cfunits.__file__))
    print('')

    run_test_suite()

