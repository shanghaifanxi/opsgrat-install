#!/bin/bash

yum install python-devel -y
if [ `command -v pip` ];then
    echo 'pip 已经安装'
else
    wget https://bootstrap.pypa.io/get-pip.py
    python get-pip.py
fi
if [ `command -v gcc` ];then
    echo 'gcc 已经安装'
else
    yum install gcc -y
fi
pip install ansible==2.8.2
yum install sshpass -y
cd install
pip install -r req.txt
python manage.py migrate
python manage.py runserver 0.0.0.0:8000

