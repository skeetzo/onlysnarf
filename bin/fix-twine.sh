#!/usr/bin/env bash
# 12/13/2019 - Skeetzo
# fixes outdated twine issue for uploading long_description w/ markdown
pip install -U twine wheel setuptools
bin/check.sh