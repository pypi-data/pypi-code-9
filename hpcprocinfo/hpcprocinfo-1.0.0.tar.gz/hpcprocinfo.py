#!/usr/bin/env python
"""Command line script designed for checking the stats of
high-performance-computing (cluster) jobs.

Given a root process ID, it will show that process and all sub-processes in a
tree, and a tabular overview of the used resources for each process. This
allows to monitor how closely the resources of a given process match the
requested resources, and whether the job is running with good CPU efficiency.
"""
import sys
import time
from collections import OrderedDict
from functools import partial
try:
    from shlex import quote
except ImportError:
    from pipes import quote
import click
from click import echo
import psutil

__version__ = '1.0.0'

DEFAULT_NAME_WIDTH = 20
DEFAULT_SHOW_THREADS = True

CPU_COUNT = psutil.cpu_count()
CPUD = len(str(CPU_COUNT)) # digits in CPU_COUNT

FIELDS = OrderedDict([ # list of all known field names
    ('cpu',   {'width':9,            'value':lambda p: time_str(cputime(p)),   'help':"CPU time"}),
    ('wall',  {'width':9,            'value':lambda p: time_str(walltime(p)),  'help':"wallclock time"}),
    ('cpw',   {'width':CPUD+2,       'value':lambda p: cpu_ratio(p),           'help':"ratio CPU time / wallclock time"}),
    ('aff',   {'width':CPUD*2+1,     'value':lambda p: affinity(p),            'help':"affinity (number of allowed CPUs / number of available CPUs)"}),
    ('thr',   {'width':max(3, CPUD), 'value':lambda p: "%d" % p.num_threads(), 'help':"number of threads"}),
    ('rss',   {'width':6,            'value':lambda p: memory_usage(p),        'help':"used RAM"}),
    ('read',  {'width':6,            'value':lambda p: read_bytes(p),          'help':"amount of data read from disk"}),
    ('write', {'width':6,            'value':lambda p: written_bytes(p),       'help':"amount of data written to disk"}),
])

DEFAULT_FIELDS = ['cpu', 'wall', 'cpw', 'thr', 'rss', 'write']


def cputime(p):
    """Return CPU time in seconds"""
    return sum(p.cpu_times())


def walltime(p):
    """Return wall time in seconds"""
    return time.time() - p.create_time()


def time_str(seconds):
    """Convert seconds into formatted string HH:MM:SS"""
    hours, remainder = divmod(seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    return '%02d:%02d:%02d' % (hours, minutes, seconds)


def cpu_ratio(p):
    """return ratio of cpu time to wall time as a formatted string"""
    return "%.1f" % (cputime(p)/walltime(p))


def human_bytes(bytes, suffix=''):
    """Given a number of bytes, determine the most appropriate (binary) prefix
    and convert to a formatted string with one decimal place

    >>> echo(human_bytes(100))
    100.0b
    >>> echo(human_bytes(1020.234))
    1020.2b
    >>> echo(human_bytes(1024))
    1.0K
    >>> echo(human_bytes(102923234))
    98.2M
    >>> echo(human_bytes(1024*102923234))
    98.2G
    >>> echo(human_bytes(1024*102923234, suffix='b'))
    98.2Gb
    >>> echo(human_bytes(1e20))
    86.7E
    >>> echo(human_bytes(1.234e50))
    102074087589043621836357632.0Y
    """
    num = bytes
    units = ['b','K','M','G','T','P','E','Z', 'Y']
    for unit in units[:-1]:
        if abs(num) < 1024.0:
            return "%3.1f%s%s" % (num, unit, suffix)
        num /= 1024.0
    return "%.1f%s%s" % (num, units[-1], suffix)


def read_bytes(p):
    """Return the amount of data read by the given process, in a human
    readable form (i.e., as a formatted string, see `human_bytes`)"""
    try:
        return human_bytes(p.io_counters().read_bytes)
    except psutil.Error:
        return 'N/A'


def written_bytes(p):
    """Return the amount of data written by the given process, in a human
    readable form (i.e., as a formatted string, see `human_bytes`)"""
    try:
        return human_bytes(p.io_counters().write_bytes)
    except psutil.Error:
        return 'N/A'


def memory_usage(p):
    """Return the RSS memory usage of the given process, in a human
    readable form (i.e., as a formatted string, see `human_bytes`)"""
    try:
        return human_bytes(p.memory_info().rss)
    except psutil.Error:
        return 'N/A'


def process_name(p, level, width=DEFAULT_NAME_WIDTH, short=False):
    """Return an indented process name, with the given total string width.
    The level specifies the number of spaces to be used for indentation"""
    indent = " "*level
    fmt = "{:<.%ss}" % (width-len(indent))
    if short:
        return indent + p.name()
    else:
        cmdline = " ".join([quote(part) for part in p.cmdline()])
        return indent + fmt.format(cmdline)


def affinity(p):
    """Return a string that gives the affinity of a process (number of CPUs on
    which the process is allowed to run over the total number of availabel
    CPUs)"""
    n = len(p.cpu_affinity())
    return "%d/%d" % (n, CPU_COUNT)


def print_process(p, level, name_width=DEFAULT_NAME_WIDTH, short_name=False,
        fields=None):
    """Print information for the given process ID"""
    name_fmt = r'{{:<{w}.{w}s}}'.format(w=name_width)
    if fields is None:
        fields = DEFAULT_FIELDS
    if level == 0: # write a header
        headers = ["{:>8s}".format('pid'), name_fmt.format('name')]
        for field in fields:
            fmt = "{name:>%ds}"%FIELDS[field]['width']
            headers.append(fmt.format(name=field))
        echo(" ".join(headers))
    values = ["{:>8d}".format(p.pid),
              name_fmt.format(
                  process_name(p, level, width=name_width, short=short_name))]
    for field in fields:
        fmt = "{{:>{width:d}.{width:d}s}}".format(width=FIELDS[field]['width'])
        value = fmt.format(FIELDS[field]['value'](p))
        values.append(value)
    echo(" ".join(values))


def print_thread(tid, i_thread, level, user_time, system_time,
        name_width=DEFAULT_NAME_WIDTH):
    """Print information about the given thread"""
    name_fmt = r'{{:<{w}.{w}s}}'.format(w=name_width)
    echo(" ".join([
        "{:> 8d}".format(tid),
        name_fmt.format(" "*level + "thread %d" % i_thread),
        "user:", "{:>10.10s}".format(time_str(user_time)),
        "system:", "{:>10.10s}".format(time_str(system_time)),
    ]))


def print_process_tree(process, level=0, process_printer=None,
        thread_printer=None, show_threads=True, user=None):
    """Print a process tree for the given process an all subprocesses

    Arguments
    ---------

    process: psutil.Process
        Process for which to print the tree

    level: int
        recursion level, for subprocesses. Should always be 0

    process_printer: callable
        routine that receives process and level, and prints an appropriate
        string to standard output. Defaults to `print_process`

    thread_printer: callable
        routine that receives a thread ID, a thread index, thread user time,
        and thread system time, and prints an appropriate string to standard
        output. Defaults to `print_thread`

    show_threads: boolean
        If True, show thread information for processes that consist of more
        than a single thread

    user: str or None
        Only print processes owned by the given user. If None, print all
        processes.
    """
    if process_printer is None:
        process_printer = print_process
    if thread_printer is None:
        thread_printer = print_thread
    try:
        process_printer(process, level)
    except psutil.Error as e:
        echo((" "*level)+str(e))
    if show_threads:
        if process.num_threads() > 1:
            for i, thread in enumerate(process.threads()):
                thread_printer(thread.id, i, level+1, thread.user_time,
                               thread.system_time)
    for sub_process in process.children():
        if (user is None) or (user == sub_process.username()):
            print_process_tree(sub_process, level=level+1,
                            process_printer=process_printer,
                            thread_printer=thread_printer,
                            show_threads=show_threads)


def process_fields(fields):
    """Clean up the list of fields obtained from command line flags

    >>> process_fields([])
    ['cpu', 'wall', 'cpw', 'thr', 'rss', 'write']
    >>> process_fields(['+rss, -cpu', '+wall'])
    ['wall', 'cpw', 'thr', 'rss', 'write']
    >>> process_fields(['rss', 'cpu'])
    ['rss', 'cpu']
    >>> process_fields(['rss, cpu', 'wall'])
    ['rss', 'cpu', 'wall']
    >>> process_fields(['+rss, cpu', 'wall'])
    ['rss', 'cpu', 'wall']
    >>> process_fields(['+aff',])
    ['cpu', 'wall', 'cpw', 'thr', 'rss', 'write', 'aff']
    >>> process_fields(['+aff',])
    ['cpu', 'wall', 'cpw', 'thr', 'rss', 'write', 'aff']
    >>> process_fields(['cpu,wall,rss', '-rss'])
    ['cpu', 'wall']
    """
    if len(fields) == 0:
        return DEFAULT_FIELDS
    separate_fields = []
    for field_item in fields:
        separate_fields += [f.strip() for f in field_item.split(",")]
    is_relative = lambda f: (f.startswith('+') or f.startswith('-'))
    relative = [is_relative(f) for f in separate_fields]
    if all(relative):
        processed_fields = OrderedDict([(f, None) for f in DEFAULT_FIELDS])
    else:
        processed_fields = OrderedDict()
    for field in separate_fields:
        if field.startswith('-'):
            del processed_fields[field[1:]]
        else:
            if field.startswith('+'):
                field = field[1:]
            processed_fields[field] = None
    for field in processed_fields:
        if not field in FIELDS:
            raise ValueError("Unknown field '%s'" % field)
    return list(processed_fields.keys())


def test(ctx, param, value):
    """Run doctests"""
    if not value or ctx.resilient_parsing:
        return
    import doctest
    doctest.testmod(verbose=True)
    ctx.exit()


def epilog():
    """Return the epilogue documentation"""
    result = "\nFIELDS\n\n\b\n"
    maxlength = max(len(s) for s in FIELDS)
    field_fmt = "{name:<%ds} {help}\n" % (maxlength+1)
    for field in FIELDS:
        result += field_fmt.format(name=field+":", help=FIELDS[field]['help'])
    result += "\nBy default, the following fields are shown: "
    result += ", ".join(DEFAULT_FIELDS)
    return result



@click.command(epilog=epilog())
@click.option('--user', '-u', metavar='USER',
    help="Limit processes to those owned by the given user")
@click.option('--name-width', '-w', type=click.INT, default=20,
    help="Width of column in which to show process name")
@click.option('--short-name', '-s', is_flag=True,
    help="Show only process 'base' names instead of full command")
@click.option('--fields', '-f', metavar='FIELDS', multiple=True,
    help="Fields to show for each process. May be given multiple times, or "
    "a single argument may contain several comma-separated list of field "
    "names. See below for valid field names. Field names may be prefixed with "
    "'+' or '-' to add to or remove from the default list of fields.")
@click.option('--test', is_flag=True, callback=test, expose_value=False,
    help="Run doctests and exit", is_eager=True)
@click.option('--threads/--no-threads', default=DEFAULT_SHOW_THREADS,
    help="Show a list of threads for processes with more than one thread")
@click.help_option('--help', '-h')
@click.version_option(version=__version__)
@click.argument('pid', type=click.INT)
def main(pid, name_width, threads, short_name, user, fields):
    """Print a process tree for the given process ID and all subprocesses.

    For each process, information relavant for a high-performance-computing
    context (i.e., CPU usage, memory usage, disk I/O) are shown.
    """
    try:
        fields = process_fields(fields)
    except ValueError as e:
        echo("FATAL ERROR: %s" % e, file=sys.stderr)
    process_printer = partial(print_process, name_width=name_width,
                              short_name=short_name, fields=fields)
    thread_printer = partial(print_thread, name_width=name_width)
    try:
        p = psutil.Process(pid)
        print_process_tree(p, level=0, process_printer=process_printer,
                           thread_printer=thread_printer, show_threads=threads,
                           user=user)
        return 0
    except psutil.Error as e:
        echo("FATAL ERROR: %s" % e, file=sys.stderr)
        return 1



if __name__ == "__main__":
    sys.exit(main())
