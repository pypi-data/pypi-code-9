import os
from pprint import pprint
from fabric.api import *
from weaver.utils import _
#TODO: my attempt at refactoring. bears some more thought
from weaver.tasks import *
from weaver.service_registry import ServiceRegistry

__all__ = ['stage', 'service', 'debug', 'ServiceRegistry']

