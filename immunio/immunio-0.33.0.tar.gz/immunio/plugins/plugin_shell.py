from __future__ import (
    print_function
)
from functools import wraps
import os

from immunio.context import get_context
from immunio.logger import log


# Set plugin name so it can be enabled and disabled.
NAME = "shell"


def add_hooks(run_hook, get_agent_func=None):
    """
    Add hooks for shell commands.
    """
    hook_os_popen(run_hook)


def hook_os_popen(run_hook):
    """
    Add our hook into os.popen
    """
    orig_os_popen = os.popen

    # Replace the original 'os.popen'
    @wraps(orig_os_popen)
    def our_os_popen(*args, **kwargs):
        log.debug("os.popen(%(args)s, %(kwargs)s)", {
            "args": args,
            "kwargs": kwargs,
            })
        _, loose_context, stack, _ = get_context()
        run_hook("file_io", {
            "method": "os.popen",
            "parameters": args,
            "information": kwargs,
            "stack": stack,
            "context_key": loose_context,
            "cwd": os.getcwd()
        })
        return orig_os_popen(*args, **kwargs)

    # Replace original with our version
    os.popen = our_os_popen
