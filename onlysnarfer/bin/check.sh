#!/usr/bin/env bash
rm -rf dist/ build/ *.egg-info
python3 setup.py sdist bdist_wheel
twine check dist/*