#!/usr/bin/env python
"""
gpw - gnuplot wrapper module for interfacing Python with gnuplot.
------------------------------------------------------------------------------------
by Wicher Minnaard <wicher@gavagai.eu> <http://smorgasbord.gavagai.nl>

This is public domain software.

Difference with gnuplot-py: This module does not need numpy. Also, this module 
doesn't offer tight integration with gnuplot.

The main problem this module solves is that gnuplot needs a) data, b) instructions,
and generates c) graph output. a) comes from files, b) can be fed in stdin, and c)
can be written to stdout and used in your Python code.

For instance, you may want to feed data from Python into gnuplot according to
some dynamically generated instructions, catch some SVG back in a Python string, 
and push that out over HTTP without messing with temporary files.

But if you want to feed _data_ from Python into gnuplot, then you must use temporary
files because stdin is reserved for instructions.

This module employs filesystem FIFOs and doesn't write data to disk.

To pull this off, the magic string 'gpw_DATAFILE_gpw' in your gnuplot instructions
(from file or as string argument) will be replaced by the filename of the fifo.
So don't name your axes that way.
And if you want to access the graph your plotscript generated from within
Python, set/leave your gnuplot output to/at stdout.
Have a look at test() for an example.
"""


import os
import subprocess
import tempfile
import threading
import sys

PY3 = (sys.version_info.major == 3)


def _mkfifo(name):
    tmpdir = tempfile.mkdtemp()
    os.mkfifo(os.path.join(tmpdir, name))
    return (tmpdir, name)


def _rmfifo(fifoinfo):
    os.remove(os.path.join(*fifoinfo))
    os.rmdir(fifoinfo[0])


def which(executable):
    """
    Finds executable in PATH environment variable
    """
    for dirname in os.environ['PATH'].split(os.path.pathsep):
        trypath = os.path.join(dirname, executable)
        if os.path.isfile(trypath) and os.access(trypath, os.X_OK):
            return trypath


def _frotdata(fifo, data):
    with open(fifo, 'wb') as fifo_fh: #blocks until other end of fifo is read
        fifo_fh.write(data)


def _mkplot_fromfile(plotscript_template, fifo_fname):
    with open(plotscript_template, 'rb') as plotscript_template_fh:
        return _magic2fifo(plotscript_template_fh.read(), fifo_fname)


def _magic2fifo(template, fifo_fname):
    if PY3:
        return (template.decode().replace('gpw_DATAFILE_gpw', fifo_fname)).encode()
    else:
        return template.replace('gpw_DATAFILE_gpw', fifo_fname)


def _rungnuplot(gppath, plotscript):
    gpproc = subprocess.Popen('', executable=gppath, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    output = gpproc.communicate(plotscript)
    return output[0]


def plot(data, gnuplotpath=None, plotscriptfile=None, plotscript=None, usefifo=True):
    """
    Feeds data and plotting instructions to GNUplot, returns GNUplot output (hopefully, a graph).
    """

    assert type(data) == bytes
    if plotscript:
        assert type(plotscript) == bytes

    plotout = None
    fifoinfo = _mkfifo('datafifo') if usefifo else (tempfile.mkdtemp(), 'datafifo')
    fifo = os.path.join(*fifoinfo)
    plotins = _mkplot_fromfile(plotscriptfile, fifo) if plotscriptfile else _magic2fifo(plotscript, fifo)
    gnuplotpath = gnuplotpath if gnuplotpath else which('gnuplot')
    if not gnuplotpath:
        raise Exception('GNUplot executable not specified, and not found on your $PATH')

    # Why use threads? Well, writing to the fifo will block until the other end gets opened
    # by GNUplot. But executing GNUplot will block until something is written to
    # the fifo. So, to be in two places at the same time, we need to split the execution.
    frotter = threading.Thread(target=_frotdata, args=(fifo, data))
    frotter.start()
    plotout = _rungnuplot(gnuplotpath, plotins)
    frotter.join()
    
    _rmfifo(fifoinfo)
    return plotout


def test():
    symbols = tuple(['\u263c', '\u2603']*2) if PY3 else tuple(['\xe2\x98\xbc', '\xe2\x98\x83']*2)

    # My locale.getpreferredencoding() is UTF-8. That's the py3 default.
    # If you don't use UTF-8, ask yourself why, and don't expect proper
    # snowman and sun symbols in the gnuplot output.
    plotscript = """
    set terminal svg

    set title "Baffling: %s melts %s"
    set xlabel "Hours of %s" textcolor rgbcolor "dark-blue"
    set ylabel "Occurrence of %s"  textcolor rgbcolor "dark-blue"
    
    set style line 11 linecolor rgbcolor "dark-blue" linewidth 3
    
    set border 4053 linestyle 11
    set lmargin 10
    
    set noxtics
    set noytics
    
    plot "gpw_DATAFILE_gpw" title "" with linespoints
    """ % symbols
    # UTF-8 unicode snowman in there ^^

    plotdata = (''.join('%d\t%d\n' % (5-i, i) for i in range(5))).encode()
    if PY3:
        plotscript = plotscript.encode()
    plotout = plot(plotdata, plotscript=plotscript)
    # In py3, the output is bytes type. In py2, it's str.
    # In thy py3 case we want to decode the bytes to print the SVG, since it's XML.
    # If you are plotting to binary terminal types (png, ps), don't decode.
    if PY3:
        plotout = plotout.decode()
    print(plotout)


if __name__ == "__main__":
    test()
