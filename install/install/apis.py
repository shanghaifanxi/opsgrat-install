# -*- coding:utf-8 -*-
from django.db import transaction
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
import os, subprocess, psutil
from install import settings
import yaml,re
from rest_framework.permissions import AllowAny


"""
安装程序
"""

@transaction.atomic()
@api_view(['POST'])
@permission_classes((AllowAny,))
def setup(request):

    opsgrat_user = request.POST.get('opsgrat_user')
    opsgrat_group = request.POST.get('opsgrat_group')
    install_dir = request.POST.get('install_dir')
    log_dir = request.POST.get('log_dir')
    pid_dir = request.POST.get('pid_dir')

    mysql_host = request.POST.get('mysql_host')
    mysql_port = request.POST.get('mysql_port')
    mysql_user = request.POST.get('mysql_user')
    mysql_user_password = request.POST.get('mysql_user_password')
    mysql_opsgrat_db = request.POST.get('mysql_opsgrat_db')
    mysql_sso_db = request.POST.get('mysql_sso_db')

    opsgrat_uwsgi_port = request.POST.get('opsgrat_uwsgi_port')
    opsgrat_nginx_port = request.POST.get('opsgrat_nginx_port')
    sso_nginx_port = request.POST.get('sso_nginx_port')
    sso_uwsgi_port = request.POST.get('sso_uwsgi_port')

    redis_host = request.POST.get('redis_host')
    redis_port = request.POST.get('redis_port')
    redis_passwd = request.POST.get('redis_passwd')

    rabbitmq_host = request.POST.get('rabbitmq_host')
    rabbitmq_port = request.POST.get('rabbitmq_port')
    rabbitmq_user = request.POST.get('rabbitmq_user')
    rabbitmq_passwd = request.POST.get('rabbitmq_passwd')

    data = ['opsgrat_user:' + ' ' + opsgrat_user, 'opsgrat_group:' + ' ' + opsgrat_group, 'install_dir:' + ' ' + install_dir, 'log_dir:' + ' ' + log_dir, 'pid_dir:' + ' ' + pid_dir + '\n',
            'mysql_host:' + ' ' + mysql_host, 'mysql_port:' + ' ' + mysql_port, 'mysql_user:' + ' ' + mysql_user, 'mysql_user_password:' + ' ' + mysql_user_password, 'mysql_opsgrat_db:' + ' ' + mysql_opsgrat_db, 'mysql_sso_db:' + ' ' + mysql_sso_db + '\n',
            'opsgrat_uwsgi_port:' + ' ' + opsgrat_uwsgi_port, 'opsgrat_nginx_port:' + ' ' + opsgrat_nginx_port, 'sso_nginx_port:' + ' ' + sso_nginx_port, 'sso_uwsgi_port:' + ' ' + sso_uwsgi_port + '\n',
            'redis_host:' + ' ' + redis_host, 'redis_port:' + ' ' + redis_port, 'redis_passwd:' + ' ' + redis_passwd + '\n',
            'rabbitmq_host:' + ' ' + rabbitmq_host, 'rabbitmq_port:' + ' '+ rabbitmq_port, 'rabbitmq_user:' + ' ' + rabbitmq_user, 'rabbitmq_passwd:' + ' ' + rabbitmq_passwd
            ]

    curDir = "{0}/".format(settings.BASE_DIR.rstrip("/"))

    if not os.path.exists(curDir):
        os.makedirs(curDir)

    fileName = 'var.yaml'
    filePath = curDir + fileName
    print('\n'.join(data))
    with open(filePath, "wb") as f:

        f.write('\n'.join(data))

    fileName = 'var.yaml'
    fileNameLog = 'opsgrat_setup.log'
    filePathLog = curDir + fileNameLog
    filePath = curDir + fileName
    os.path.dirname("{0}".format(settings.BASE_DIR.rstrip("/")))
    os.chdir(os.path.dirname("{0}".format(settings.BASE_DIR.rstrip("/"))))
    command ='nohup ansible-playbook -i local main.yml -e @' + filePath + ' ' + ' > ' + filePathLog + " &"
    subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    res = os.popen("ps -ef|grep ansible-playbook | grep var.yaml | grep -v 'grep'| awk '{print $2}'")
    pid = res.read()

    fileCheckName = "check.txt"
    filePathCheck = curDir + fileCheckName
    with open(filePathCheck, 'wb') as pc:
            pc.write(str(pid))

    response = Response({"success": True, "msg": "succ", "data": data})
    response.content_type = "text/html;charset=utf-8"
    return response


"""
检查进程
"""

@transaction.atomic()
@api_view(['GET'])
def check(request):

    log = ""
    msg = ""
    curDir = "{0}/".format(settings.BASE_DIR.rstrip("/"))
    fileNameLog = 'opsgrat_setup.log'
    filePathLog = curDir + fileNameLog
    path = "{0}/opsgrat_setup.log".format(settings.BASE_DIR.rstrip("/"))
    if os.path.exists(path):
        with open(path, 'r') as f:
            log = f.read()

    fileCheckName = "check.txt"
    filePathCheck = curDir + fileCheckName
    if os.path.exists(filePathCheck):
        with open(filePathCheck, 'r') as cf:
            checks = cf.readlines()

            try:
                for check in checks:
                    if psutil.Process(int(check)).is_running() == True:
                        msg = True
                        break
            except:
                msg = False
    print msg

    if msg == False and os.path.exists(filePathCheck):
        os.remove(filePathCheck)

    with open(filePathLog, 'r') as f:
        content = f.read()
        pattern = re.compile(r'(?<=failed=)\d+\.?\d*')
        check_logs = pattern.findall(content)
    if msg == False and check_logs[0] > 0:
        result = False
    elif msg == False and check_logs == []:
        result = 'null'
    else:
        result = True

    response = Response({"success": True, "msg": 'succ', "is_running": msg, "log": log, "result": result})
    response.content_type = "text/html;charset=utf-8"

    return response


"""
Ansible安装
"""
@transaction.atomic()
@api_view(['POST'])
def setupAnsible(request):

    command = 'pip install ansible'
    subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    res = os.popen("ps -ef|grep ansible | grep pip  | grep -v 'grep'| awk '{print $2}'")
    pid = res.read()

    curDir = "{0}/".format(settings.BASE_DIR.rstrip("/"))
    CheckAnsibleName = "check_ansible.txt"
    PathCheckAnsible = curDir + CheckAnsibleName
    with open(PathCheckAnsible, 'wb') as pc:
            pc.write(str(pid))

    response = Response({"success": True, "msg": 'succ', "pid": pid})
    response.content_type = "text/html;charset=utf-8"

    return response


@transaction.atomic()
@api_view(['GET'])
def ansible(request):

    result = ""
    curDir = "{0}/".format(settings.BASE_DIR.rstrip("/"))
    CheckAnsibleName = "check_ansible.txt"
    PathCheckAnsible = curDir + CheckAnsibleName
    if os.path.exists(PathCheckAnsible):
        with open(PathCheckAnsible, 'r') as cf:
            checks = cf.readlines()

            try:
                for check in checks:
                    if psutil.Process(int(check)).is_running() == True:
                        result = True
                        break
            except:
                result = False

    if result == False and os.path.exists(PathCheckAnsible):
        os.remove(PathCheckAnsible)
    response = Response({"success": True, "msg": 'succ', "result": result})
    response.content_type = "text/html;charset=utf-8"

    return response



"""
SSHPASS安装
"""
@transaction.atomic()
@api_view(['POST'])
def setupSshPass(request):

    command = 'pip install sshpass'
    subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    res = os.popen("ps -ef|grep pip | grep sshpass| grep -v 'grep'| awk '{print $2}'")
    pid = res.read()

    curDir = "{0}/".format(settings.BASE_DIR.rstrip("/"))
    CheckSshPassName = "check_sshpass.txt"
    PathCheckSshPass = curDir + CheckSshPassName
    with open(PathCheckSshPass, 'wb') as pc:
            pc.write(str(pid))

    response = Response({"success": True, "msg": 'succ', "pid": pid})
    response.content_type = "text/html;charset=utf-8"

    return response


@transaction.atomic()
@api_view(['GET'])
def sshpass(request):

    result = ""
    curDir = "{0}/".format(settings.BASE_DIR.rstrip("/"))
    CheckSshPassName = "check_sshpass.txt"
    PathCheckSshPass = curDir + CheckSshPassName
    if os.path.exists(PathCheckSshPass):
        with open(PathCheckSshPass, 'r') as cf:
            checks = cf.readlines()

            try:
                for check in checks:
                    if psutil.Process(int(check)).is_running() == True:
                        result = True
                        break
            except:
                result = False

    if result == False and os.path.exists(PathCheckSshPass):
        os.remove(PathCheckSshPass)
    response = Response({"success": True, "msg": 'succ', "result": result})
    response.content_type = "text/html;charset=utf-8"

    return response


"""
停止安装
"""

@transaction.atomic()
@api_view(['POST'])
def stopPid(request):

    res = os.popen("ps -ef|grep ansible-playbook | grep var.yaml | grep -v 'grep'| awk '{print $2}'")
    pids = res.readlines()
    for pid in pids:
        command = 'kill -9' + ' ' + pid
        subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

    response = Response({"success": True, "msg": 'succ', "pid": pids})
    response.content_type = "text/html;charset=utf-8"

    return response
