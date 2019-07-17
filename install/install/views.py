# -*- coding: utf-8 -*-
from django.views.generic import TemplateView
from whichcraft import which
from install import settings
import os,yaml,re
from django.http import HttpResponseRedirect


def SetupIndex(request):
    return HttpResponseRedirect('/setup/')


class SetupView(TemplateView):

    template_name = "setup.html"

    def get_context_data(self, **kwargs):

        context = super(SetupView, self).get_context_data(**kwargs)

        if which('python') != '':
            context['python'] = which('python')
        else:
            context['nopython'] = None

        if which('ansible') != '':
            context['ansible'] = which('ansible')
        else:
            context['noansible'] = None

        if which('pip') != '':
            context['pip'] = which('pip')
        else:
            context['nopip'] = None

        if which('sshpass') != '':
            context['sshpass'] = which('sshpass')
        else:
            context['nosshpass'] = None

        # if which('mysql') != '':
        #     context['mysql'] = which('mysql')
        # else:
        #     context['nomysql'] = None

        name = "var.yaml"
        curDir = "{0}/".format(settings.BASE_DIR.rstrip("/"))
        path = curDir + name
        if os.path.exists(path):
            with open(path ,'r') as f:
                file = yaml.load(f)
                context['file'] = file
        return context
