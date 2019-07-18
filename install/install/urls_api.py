from django.conf.urls import url
from install import apis

urlpatterns = [
    url('setup/$', apis.setup, name='api_setup'),

    url('check/$', apis.check, name='api_check'),

    url('setup/ansible/$', apis.setupAnsible, name='api_setup_ansible'),

    url('ansible/$', apis.ansible, name='api_ansible'),

    url('setup/sshpass/$', apis.setupSshPass, name='api_setup_sshpass'),

    url('sshpass/$', apis.sshpass, name='api_sshpass'),

    url('stop/pid/$', apis.stopPid, name='api_stop_pid'),
    ]
