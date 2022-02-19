#!/usr/bin/env bash
# fixes outdated twine issue for uploading long_description w/ markdown
pip install -U twine wheel setuptools
bin/check.sh