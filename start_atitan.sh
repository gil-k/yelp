#!/usr/bin/env bash
cd /home/ubuntu/atitan
virtualenv venv
. venv/bin/activate
pip install Flask
python index.py
