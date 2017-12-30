#!/bin/bash

PYPACKAGE=`python setup.py sdist | egrep 'creating'|head -1 | sed 's/creating\s*//g'`;
PYPACKAGE="dist/$PYPACKAGE.tar.gz";
echo "Uploading $PYPACKAGE to PyPI";
twine upload "$PYPACKAGE";
