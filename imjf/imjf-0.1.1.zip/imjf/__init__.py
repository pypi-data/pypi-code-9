""" The official Python client for www.isMyJsFucked.com """

from .client import ismyjsfucked, report
from .exceptions import IMJFException

__all__ = ['ismyjsfucked',
           'report',
           'IMJFException']

