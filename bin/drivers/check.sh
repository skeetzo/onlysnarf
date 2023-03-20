#!/usr/bin/env bash
python -m build
twine check dist/*