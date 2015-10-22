import sys

from .cli import cli
from .resource import PlutResource
from .utils import get_or_create_port

__all__ = ['port', 'services']


def port(service):
    return get_or_create_port(PlutResource(), service)


def services():
    return iter(PlutResource())
