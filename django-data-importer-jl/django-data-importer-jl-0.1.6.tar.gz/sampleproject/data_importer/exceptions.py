# coding: utf-8
from __future__ import unicode_literals
from __future__ import print_function
from __future__ import division
from __future__ import absolute_import
from future import standard_library
standard_library.install_aliases()
from builtins import *
from django.utils.translation import ugettext_lazy as _

class UnknowSource(Exception):
    msg = _(u"The source file can't be opened")
    def __init__(self,err=None):
        if err:
            self.msg = _(u"%(msg)s, the error was: %(err)s") % {'msg':self.msg,'err':err}

