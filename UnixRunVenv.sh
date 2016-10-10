#!/bin/bash
pip3 install virtualenv
source venv/bin/activate
venv/bin/python ./Activities/manage.py makemigrations
venv/bin/python ./Activities/manage.py migrate
venv/bin/python ./Activities/manage.py runserver localhost:666
