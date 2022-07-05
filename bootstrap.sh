#!/bin/bash

sudo apt -y install python3-pip python3-setuptools unzip
sudo pip3 install virtualenv
virtualenv -p python3 ~/venv
source ~/venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt