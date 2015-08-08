import contextlib
import errno
import functools
import logging
import grp
import os
import pwd
import sys
import threading


def graceful_interrupt(return_value, logger_name=None):
    """Method decorator that gracefully catches system interrupts and
    returns a predefined value.

    Args:
        return_value: the return value in the case of a system interrupt.
        logger_name: optionally specify a logger name.
    """
    logger = logging.getLogger(logger_name or __name__)

    def decorator_factory(func):
        @functools.wraps(func)
        def decorator(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                if getattr(e, 'errno', None) != errno.EINTR:
                    raise
                t = threading.current_thread()
                logger.warning(
                    "I/O operation interrupted in thread {0}".format(t.name)
                )
            else:
                if issubclass(return_value, Exception)\
                or isinstance(return_value, Exception):
                    raise return_value
                return return_value

        return decorator

    return decorator_factory


def require_privileged(error_message):
    """Requires a process to be run as a privileged user."""
    if os.getuid() != 0:
        print(error_message, file=sys.stderr)
        sys.exit(1)


@contextlib.contextmanager
def pidfile(filepath, daemon):
    """Create a pidfile for a process."""
    if not daemon:
        yield
    else:
        try:
            if os.path.exists(filepath):
                print("Pidfile present:", filepath,
                    file=sys.stderr)
                sys.exit(-1)
            with open(filepath, 'w') as f:
                f.write(str(os.getpid()))
            yield
            try:
                os.unlink(filepath)
            except (IOError, OSError):
                pass
        except IOError:
            print("Unable to write pidfile to {0}".format(filepath),
                file=sys.stderr)
            sys.exit(-1)


def drop_privileges(user, group=None):
    """Drops privileges to the specified user and group.

    Args:
        user (str): specifies the user.
        group (str): specifies the group; if `group` is
            ``None``, it is considered the same as
            `user`.

    Returns:
        None
    """
    if not isinstance(group, int):
        group = grp.getgrnam(group or user).gr_gid
    if not isinstance(user, int):
        user = pwd.getpwnam(user).pw_uid
    os.setgid(group)
    os.setuid(user)
