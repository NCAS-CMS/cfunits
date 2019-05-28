from __future__ import print_function

import unittest
import os
import sys

import cftime
import numpy
import datetime
import cfunits

from platform    import system, platform, python_version

# Build the test suite from the tests found in the test files.
testsuite = unittest.TestSuite()
testsuite.addTests(unittest.TestLoader().discover('.', pattern='test_*.py'))

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
    print('cftime version:'        , cftime.__version__)
    print('numpy version:'         , numpy.__version__)
    print('cfunits version:', cfunits.__version__)
    print('cfunits path:'   , os.path.abspath(cfunits.__file__))
    print('')

    run_test_suite()

