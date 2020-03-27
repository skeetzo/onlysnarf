#!/usr/bin/env bash
if [ -z "$1" ]; then
	set "upload"
fi
bin/save.sh $1
wait
rm -rf dist/ build/ *.egg-info
python3 setup.py sdist bdist_wheel
twine upload dist/*