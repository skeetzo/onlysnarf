#!/usr/bin/env bash
sudo bin/clean.sh
if [ -z "$1" ]; then
	set "saved"
fi
git add . && git commit -m "$1" && git push