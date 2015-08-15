from itertools import count
from random import randint

def census(fp):
    lines = []
    line = None

    while True:
        line_start = fp.tell()
        line = fp.readline()
        line_end = fp.tell()
        if line == '':
            break
        else:
            lines.append((line_start, line_end))

    return lines

def srs(n, fp):
    '''
    with replacement

    If data are appended to the file during the function call,
    the appended data are ignored for the sampling.
    '''
    file_start = fp.tell()
    file_end = fp.seek(0, 2)
    lines = []

    for i in count():
        fp.seek(randint(file_start, file_end))
        fp.readline()
        line_start = fp.tell()
        line = fp.readline()
        line_end = fp.tell()
        if line == '':
            pass
        elif line[-1] == '\n':
            lines.append((line_start, line_end))
        else:
            raise NotImplementedError('I can\'t handle this line:\n%s' % line)

        if len(lines) == n:
            break

        if len(lines) == 0 and i > 1000:
            raise EnvironmentError('It appears that this file contains no line breaks.')

    fp.seek(file_start)
    return lines
