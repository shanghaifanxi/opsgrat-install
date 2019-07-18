from django.conf.urls import url
from install import apis

urlpatterns = [
    url('setup/', apis.setup, name='api_setup'),

    url('check/', apis.check, name='api_check'),

    url('setupAnsible/', apis.setupAnsible, name='api_setup_ansible'),

    url('setupPip/', apis.setupPip, name='api_setup_pip'),

    url('setupSshPass/', apis.setupSshPass, name='api_setup_sshpass'),

    url('stopPid/', apis.stopPid, name='api_stop_pid'),
    ]
