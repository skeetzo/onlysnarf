#!/usr/bin/env bash
if [ -z "$1" ]; then
	set "master"
fi
bin/save.sh
wait
rm -rf dist/ build/ *.egg-info
python3 setup.py sdist bdist_wheel
twine upload dist/*