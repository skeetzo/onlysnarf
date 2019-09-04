#!/usr/bin/env bash
rm -rf dist/ build/ *.egg-info
python3 setup.py bdist_wheel
twine upload dist/*