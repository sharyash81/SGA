#!/bin/bash
systemctl start mongod
virtualenv venv
source venv/bin/activate
pip install pandas
pip install xmltodict
