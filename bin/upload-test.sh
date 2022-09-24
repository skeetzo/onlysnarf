#!/usr/bin/env bash
if [ -z "$1" ]; then
	set "upload"
fi
bin/save.sh
wait
python -m build
twine upload -r testpypi dist/*