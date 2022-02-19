# apt-get install python3-venv
python3.8 -m pip install --user virtualenv
python3.8 -m venv venv
wait
source venv/bin/activate
pip install --upgrade pip
pip install setuptools_rust
# deactivate

# virtualenv --python=/usr/bin/python3.8 venv



