""" The official Python client for www.isMyJsFucked.com """

from .client import ismyjsfucked, report
from .exceptions import IMJFException, ReportException

__all__ = ['ismyjsfucked',
           'report',
           'IMJFException',
           'ReportException']

