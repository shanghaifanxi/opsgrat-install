#!/bin/bash

yum install python-devel
if [ `command -v pip` ];then
    echo 'pip 已经安装'
else
    wget https://bootstrap.pypa.io/get-pip.py
    python get-pip.py
fi
cd install
pip install -r req.txt
python manage.py migrate
python manage.py runserver 0.0.0.0:8000

