from django.utils.module_loading import import_string
from django.conf import settings

from studiogdo.pip.admin import admin

pathpatterns = import_string("pip.admin.%s.pathpatterns" % admin.paths)
