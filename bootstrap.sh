#!/bin/bash

sudo apt -y install python3-pip python3-setuptools unzip
sudo pip3 install virtualenv
virtualenv -p python3 ~/venv
cd ~/venv/bin && activate
cd ~/slack-Unleash
pip install --upgrade pip
pip install -r requirements