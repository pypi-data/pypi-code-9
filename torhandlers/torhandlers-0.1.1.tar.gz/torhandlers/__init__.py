# -*- coding: utf-8 -*-
__author__ = 'Alex Bo'
__email__ = 'bosha@the-bosha.ru'

from .exceptions import ImproperlyConfigured
from .base import TemplateHandler, RedirectHandler
from .list import ListHandler
from .form import FormHandler
from .detail import DetailHandler
from .edit import EditHandler
from .create import CreateHandler
from .delete import DeleteHandler
