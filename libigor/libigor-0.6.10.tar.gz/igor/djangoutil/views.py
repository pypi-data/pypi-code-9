#!/usr/bin/env python2
# -*- coding: utf-8 -*-
from os.path import splitext
from django.views.generic import TemplateView
from django.conf.urls import url


#----------------------------------------------------------------------------//
def serve(tname, href = None):
    def wrappedview(req):
        view = TemplateView.as_view(template_name = tname)
        return view(req)

    return url(
        href or r'^{}$'.format(tname),
        wrappedview,
        name = splitext(tname.replace('/', '-'))[0]
    )
