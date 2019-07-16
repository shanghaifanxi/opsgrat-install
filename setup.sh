#!/bin/bash

cd install
pip install -r req.txt
python manage.py runserver 0.0.0.0:8000

