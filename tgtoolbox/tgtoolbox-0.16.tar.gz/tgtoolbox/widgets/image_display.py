# -*- coding: utf-8 -*-
import tw2.core as twc
__author__ = 'vahid'


class ImageDisplay(twc.Widget):
    value = twc.Param(default='/img/no-image-available.jpg', attribute=True, view_name='src')
    width = twc.Param(default=None, attribute=True)
    height = twc.Param(default=None, attribute=True)
    alt = twc.Param(default=None, attribute=True)
    template = 'mako:tgtoolbox.widgets.templates.image_display'