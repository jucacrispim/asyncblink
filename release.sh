#!/bin/bash

rm -rf dist/

python -m build

cd dist

fname=`ls | grep tar`

curl -F file=@$fname -F prefix=pypi/asyncblink $PYPI_UPLOAD_URL -H "Authorization: Key $TUPI_AUTH_KEY"
