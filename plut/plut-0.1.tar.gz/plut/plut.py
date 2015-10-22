import sys

from .cli import cli
from .resource import PlutResource
from .utils import get_or_create_port

__all__ = ['port']


def port(service, rcfile=None):
    return get_or_create_port(PlutResource(rcfile), service)
