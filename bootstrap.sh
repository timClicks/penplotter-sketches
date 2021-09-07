#! /bin/bash

python3 -m venv venv
source venv/bin/activate
pip install -U pip
pip install vpype[all]
pip install git+https://github.com/abey79/vsketch#egg=vsketch
