#!/usr/bin/env bash
if [ -z "$1" ]; then
	set "upload"
fi
python -m pip freeze
bin/save.sh
wait
python -m build
twine upload dist/*