from django.conf.urls import url
from install import apis

urlpatterns = [
    url('setup/', apis.setup, name='api_setup'),

    url('check/', apis.check, name='api_check'),
    ]
