#!/usr/bin/env bash
cd /home/ubuntu/atitan
virtualenv BASELINE
. BASELINE/bin/activate
pip install Flask
python atitan.py
