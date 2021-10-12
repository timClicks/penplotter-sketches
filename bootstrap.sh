#! /bin/bash

python3 -m venv venv
source venv/bin/activate
pip install -U pip
pip install -r requirements.txt
pip install git+https://github.com/abey79/vsketch#egg=vsketch
