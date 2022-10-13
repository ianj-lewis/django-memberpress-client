#!/bin/sh
#------------------------------------------------------------------------------
# written by: Lawrence McDaniel
#             https://lawrencemcdaniel.com
#
# date:       oct-2022
#
# usage:      a work in progress. build package and upload to PyPi.
#             https://pypi.org/project/edx-memberpress-client/
#------------------------------------------------------------------------------

python3 -m pip install --upgrade setuptools wheel twine
python -m pip install --upgrade build

sudo rm -r build
sudo rm -r dist
sudo rm -r edx_memberpress_client.egg-info

python3 -m build --sdist ./
python3 -m build --wheel ./

python3 -m pip install --upgrade twine
twine check dist/*
