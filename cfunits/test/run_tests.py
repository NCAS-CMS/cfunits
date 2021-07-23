from __future__ import print_function

import datetime
import doctest
import faulthandler
import os
import pkgutil
import sys
import unittest
from platform import platform, python_version
from random import choice

import numpy

faulthandler.enable()  # to debug seg faults and timeouts

import cftime

import cfunits


def randomise_test_order(*_args):
    """Returns a random choice from 1 or -1.

    When set as the test loader method for standard (merge)sort
    comparison to order all methods in a test case (see
    'sortTestMethodsUsing'), ensures they run in a (semi-)random order,
    meaning implicit reliance on setup or state, i.e. test dependencies,
    should become evident over repeated runs.

    """
    return choice([1, -1])


test_loader = unittest.TestLoader
# Randomise the order to run the specific test_Units_* methods
test_loader.sortTestMethodsUsing = randomise_test_order

# Build the test suite from the tests found in the test files.
testsuite = unittest.TestSuite()
testsuite.addTests(
    test_loader().discover(
        os.path.dirname(os.path.realpath(__file__)), pattern="test_*.py"
    )
)

# Include doctests
testsuite_doctests = unittest.TestSuite()
# Tell doctest comparisons to treat any sequence of whitespace including
# newlines as equal and to take '...' in output to mean anything can be there
doctest_flags = doctest.NORMALIZE_WHITESPACE | doctest.ELLIPSIS
for importer, name, ispkg in pkgutil.walk_packages(
    cfunits.__path__, cfunits.__name__ + "."
):
    testsuite.addTests(doctest.DocTestSuite(name, optionflags=doctest_flags))


def run_test_suite(verbosity=2):
    """Runs the test suite."""
    runner = unittest.TextTestRunner(verbosity=verbosity)
    outcome = runner.run(testsuite)
    # Note unittest.TextTestRunner().run() does not set an exit code, so (esp.
    # for CI / GH Actions workflows) we need $? = 1 set if any sub-test fails:
    if not outcome.wasSuccessful():
        exit(1)  # else is zero for sucess as standard


if __name__ == "__main__":
    print("------------------")
    print("CFUNITS TEST SUITE")
    print("------------------")
    print("Run date:", datetime.datetime.now())
    print("Platform:", str(platform()))
    print("python:", str(python_version() + " " + str(sys.executable)))
    print("cftime version:", cftime.__version__)
    print("numpy version:", numpy.__version__)
    print("cfunits version:", cfunits.__version__)
    print("cfunits path:", os.path.abspath(cfunits.__file__))
    print("")
    print("Running tests from", os.path.abspath(os.curdir))
    print("")

    run_test_suite()
