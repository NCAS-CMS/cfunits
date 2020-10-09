* Change the version and date in `cfunits/__init__.py` (`__version__` and
  `__date__` variables)

* Make sure that `README.md` is up to date.

* Make sure that `Changelog.rst` is up to date.

* Make sure that the correct path to the cfunits library is in the
  `PYTHONPATH` environment variable:

  ```bash
  export PYTHONPATH=$PWD:$PYTHONPATH
  ```

* Build a development copy of the documentation using to check API
  pages for any new methods are present & correct, & that the overall
  formatting has not been adversely affected for comprehension by any
  updates in the latest Sphinx or theme etc. (Do not manually commit
  the dev build.)

  ```bash
  ./release_docs <vn> dev-clean # E.g. ./release_docs 3.2.6 dev-clean
  ```

* Create an archived copy of the documentation:

  ```bash
  ./release_docs <vn> archive # E.g. ./release_docs 3.2.6 archive
  ```

* Update the latest documentation:

  ```bash
  ./release_docs <vn> latest # E.g. ./release_docs 3.2.6 latest
  ```

* Create a source tarball:

  ```bash
  python setup.py sdist
  ```

* Test the tarball release using

  ```bash
  ./test_release <vn> # E.g. ./test_release 3.2.6
  ```

* Push recent commits using

  ```bash
  git push origin master
  ```

* Tag the release:

  ```bash
  ./tag <vn> # E.g. ./tag 3.2.6
  ```

* Upload the source tarball to PyPi. Note this requires the `twine`
  library (which can be installed via `pip`) and relevant project
  privileges on PyPi.

  ```bash
  ./upload_to_pypi <vn> # E.g. ./upload_to_pypi 3.2.6
  ```
