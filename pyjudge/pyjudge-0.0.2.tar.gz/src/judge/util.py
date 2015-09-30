import io
import sys
import signal
import functools
import html
from threading import Thread

_print_func = print

#
# String formmating
#


def indent(st, indent=4):
    '''Indent string by the given number of spaces or the given indentation
    string'''

    indent = ' ' * indent if isinstance(indent, int) else indent
    lines = [indent + x for x in st.splitlines()]
    return '\n'.join(lines)


def html_escape(x):
    '''Escape unsafe HTML characters such as < > & etc'''

    return html.escape(x)


#
# Special IO functions for python script interactions
#
def capture_print(*args, **kwds):
    '''A print-like function that return the formatted string instead of
    printing it on screen'''

    out, err = sys.stdout, sys.stderr
    out_io = sys.stdout = sys.stderr = io.StringIO()
    try:
        _print_func(*args, **kwds)
    finally:
        sys.stdout, sys.stderr = out, err
    return out_io.getvalue()


def make_interaction_print(interaction):
    '''Returns a print() function that instead of printing through the regular
    channels, it appends an Out string to the given list of interactions'''

    from .parsers import Out

    @functools.wraps(print)
    def print_func(*args, **kwds):
        data = capture_print(*args, **kwds)
        if interaction and isinstance(interaction[-1], Out):
            data = interaction.pop() + data
        interaction.append(Out(data))

    return print_func


def make_interaction_input(interaction, inputs):
    '''Returns an input() function that instead of asking for user input
    through the regular channels, it retrives values from the inputs list and
    saves the corresponding interaction in the interactoin list.'''

    from . import errors
    from .parsers import In, Prompt

    @functools.wraps(input)
    def input_func(msg=None):
        if msg:
            interaction.append(Prompt(msg))
        try:
            data = inputs.pop(0)
        except IndexError:

            raise errors.MissingInputError
        interaction.append(In(data))
        return data

    return input_func

#
# Execution with timeout limits
#


def __timeout_handler(signum, frame):
    '''Helper function for the timeout() function.'''

    raise TimeoutError()


def timeout(func, args=(), kwargs={}, timeout=1.0, threading=True):
    '''Execute callable `func` with timeout.

    If timeout exceeds, raises a TimeoutError'''

    if threading:
        result = []
        exceptions = []

        def target():
            try:
                result.append(func(*args, **kwargs))
            except Exception as ex:
                exceptions.append(ex)

        thread = Thread(target=target)
        thread.start()
        thread.join(timeout)
        if thread.is_alive():
            raise TimeoutError
        else:
            try:
                return result.pop()
            except IndexError:
                raise exceptions.pop()
    else:
        signal.signal(signal.SIGALRM, __timeout_handler)
        signal.alarm(timeout)
        try:
            result = func(*args, **kwargs)
        finally:
            signal.alarm(0)

        return result
