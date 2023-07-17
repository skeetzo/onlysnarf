#!/bin/bash
python -m pytest tests/api/test_api.py
pytest tests/selenium
pytest tests/snarf