from django.conf.urls import url
from install import apis

urlpatterns = [
    url('setup/', apis.setup.as_view(), name='api_setup'),

    url('check/', apis.check.as_view(), name='api_check'),

    url('setupAnsible/', apis.setupAnsible.as_view(), name='api_setup_ansible'),

    url('setupPip/', apis.setupPip.as_view(), name='api_setup_pip'),

    url('setupSshPass/', apis.setupSshPass.as_view(), name='api_setup_sshpass'),

    url('stopPid/', apis.stopPid.as_view(), name='api_stop_pid'),
    ]
