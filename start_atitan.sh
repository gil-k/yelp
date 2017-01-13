#!/usr/bin/env bash
cd /home/ubuntu/atitan
virtualenv BASELINE
. BASELINE/bin/activate
#pip install Flask
python setup.py install
#pip install requests
#pip install grequests
pip install -r requirements.txt
python atitan.py
