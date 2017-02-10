#!/usr/bin/env bash
cd /var/www/atitan/atitan
# run manually first virtualenv VENV --no-site-packages
. VENV/bin/activate # venv
#pip install Flask
# run manually first python setup.py install
#pip install requests
#pip install grequests
# pip install -r requirements.txt
python atitan.py
