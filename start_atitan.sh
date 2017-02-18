#!/usr/bin/env bash
cd /home/kd/atitan/atitan
# run manually first virtualenv VENV --no-site-packages
. venv/bin/activate
#pip install Flask
# run manually first python setup.py install
#pip install requests
#pip install grequests
# pip install -r requirements.txt
python atitan.py
