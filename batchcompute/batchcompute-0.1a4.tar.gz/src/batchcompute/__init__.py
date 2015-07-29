'''A simple implement for BatchCompute service SDK.
'''
__version__ = '0.1a2'
__all__ = [
    "Client", "JobDescription", "TaskDescription", "TaskDag", "ResourceDescription",
    "ClientError"
]
__author__ = 'crisish <helei@alibaba-inc.com>'

from .client import Client
from .resources import (
    JobDescription, TaskDescription, TaskDag, ResourceDescription
)
from .core import ClientError
