#!/bin/bash
python setup.py install
pytest tests/selenium
pytest tests/snarf