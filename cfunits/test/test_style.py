import faulthandler
import os
import unittest

import pycodestyle

faulthandler.enable()  # to debug seg faults and timeouts

import cfunits


class styleTest(unittest.TestCase):
    """Tests all Python files for PEP8 compliance."""

    def setUp(self):
        """Runs any preparatory steps to set up each test method."""
        self.cfunits_dir = os.path.dirname(os.path.abspath(__file__))
        os.chdir(self.cfunits_dir)

    def test_pep8_compliance(self):
        """Tests the codebase for compliance with the PEP8 standard."""
        pep8_check = pycodestyle.StyleGuide()

        # Directories to skip in the recursive walk of the directory:
        skip_dirs = ("__pycache__",)
        # These are pycodestyle errors and warnings to explicitly ignore. For
        # descriptions for each code see:
        # https://pep8.readthedocs.io/en/latest/intro.html#error-codes
        pep8_check.options.ignore += (  # ignored because...
            "E402",  # ...justified lower module imports in __init__ and units
            "E501",  # ...docstring examples include output lines >79 chars
            "E722",  # ...several "bare except" cases need to be addressed
        )

        # Find all Python source code ('.py') files in the 'cfunits' directory,
        # including all unskipped sub-directories within e.g. test directory:
        python_files = []
        for root_dir, dirs, filelist in os.walk(".."):  # '..' == 'cfunits/'
            if os.path.basename(root_dir) in skip_dirs:
                continue
            python_files += [
                os.path.join(root_dir, fname)
                for fname in filelist
                if fname.endswith(".py")
            ]

        pep8_issues = pep8_check.check_files(python_files).total_errors
        self.assertEqual(
            pep8_issues,
            0,
            f"Detected {pep8_issues!s} PEP8 errors or warnings:",
        )


# --- End: class


if __name__ == "__main__":
    print("cfunits version:", cfunits.__version__)
    print("cfunits path:", os.path.abspath(cfunits.__file__))
    print("")
    unittest.main(verbosity=2)
