# OpenFieldReader Python Wrapper [![PyPI version](https://badge.fury.io/py/openfieldreaderwrapper.svg)](https://badge.fury.io/py/openfieldreaderwrapper)

A wrapper around the openfieldreader command line tool to automatically detect paper-based form fields.

The algorithm run a ICR cell-detection analysis. It only focuses on paper-based forms. Because handwriting text represents valuable data. They can help automatically detect entities involved. Printed characters can be processed by tesseract.

Package installation:
- `pip install openfieldreaderwrapper`

Uninstallation:
- `pip uninstall openfieldreaderwrapper`

## Note for maintainers:

Local package installation:
- `python setup.py install`

How to upload a new package version
- In the file setup.py, change the version
- (first time only) `python -m pip install --user --upgrade setuptools wheel`
- `python setup.py sdist bdist_wheel`
- (first time only) `python -m pip install --user --upgrade twine`
- `twine upload dist/*`

# Copyright and license
Code released under the MIT license.
