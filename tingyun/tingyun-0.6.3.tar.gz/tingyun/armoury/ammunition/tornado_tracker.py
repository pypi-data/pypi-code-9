
"""this module is implement some wrapper for trace the tronado module

"""

import logging
import weakref
import sys

from tingyun.logistics.object_name import callable_name
from tingyun.battlefield.proxy import proxy_instance
from tingyun.battlefield.tracer import Tracer
from tingyun.armoury.ammunition.tracker import current_tracker
from tingyun.armoury.trigger.wsgi_tornado import process_environ
from tingyun.armoury.ammunition.function_tracker import FunctionTracker
from tingyun.logistics.basic_wrapper import FunctionWrapper


console = logging.getLogger(__name__)
