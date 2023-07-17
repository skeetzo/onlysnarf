#!/bin/sh
# -users arg is provided to squelch requirement from onlysnarf args
python ./OnlySnarf/api/index.py -verbose users

# from flask example but don't apply here:

# export FLASK_APP=./api/index.py
# export FLASK_ENV=production
# pipenv run flask --debug run -h 0.0.0.0
# FLASK_ENV=production python api/index.py users