""" goulash._os
"""
import shutil
import os
import errno
import time
import stat
from goulash.python import get_env

# copy-tree with overwrites (unlike shutil.copytree)
from distutils.dir_util import copy_tree  # NOQA
from distutils.file_util import copy_file  # NOQA

#SRC: http://stackoverflow.com/questions/566746/how-to-get-console-window-width-in-python
def get_term_size():
    import os
    env = os.environ
    def ioctl_GWINSZ(fd):
        try:
            import fcntl, termios, struct, os
            cr = struct.unpack('hh', fcntl.ioctl(fd, termios.TIOCGWINSZ,
        '1234'))
        except:
            return
        return cr
    cr = ioctl_GWINSZ(0) or ioctl_GWINSZ(1) or ioctl_GWINSZ(2)
    if not cr:
        try:
            fd = os.open(os.ctermid(), os.O_RDONLY)
            cr = ioctl_GWINSZ(fd)
            os.close(fd)
        except:
            pass
    if not cr:
        cr = (env.get('LINES', 25), env.get('COLUMNS', 80))

        ### Use get(key[, default]) instead of a try/catch
        #try:
        #    cr = (env['LINES'], env['COLUMNS'])
        #except:
        #    cr = (25, 80)
    return int(cr[1]), int(cr[0])

def rmtree(path):
    if os.path.exists(path):
        shutil.rmtree(path)


def home():
    return get_env('HOME')
get_home = home


def touch(fname, times=None):
    """ similar to shell command 'touch' """
    with open(fname, 'a'):
        os.utime(fname, times)
touch_file = touch


def file_age_in_seconds(pathname):
    if not os.path.exists(pathname):
        return None
    return time.time() - os.stat(pathname)[stat.ST_MTIME]

# SOURCE:
#  http://stackoverflow.com/questions/600268/mkdir-p-functionality-in-python


def mkdir_p(path):
    """ os.makedirs() is a constant annoyance since it is
        close to having this functionality, but always dies
        if the argument already exists
    """
    path = os.path.expanduser(path)
    try:
        os.makedirs(path)
    except OSError as exc:  # Python >2.5
        if exc.errno == errno.EEXIST and os.path.isdir(path):
            pass
        else:
            raise
    return path
makedirs = mkdirs = mkdir_p


def which(name):
    return os.popen('which ' + name).readlines()[0].strip()


def get_mounts_by_type(mtype):
    tmp = os.popen('mount -l -t {0}'.format(mtype))
    tmp = tmp.readlines()
    tmp = [x.strip() for x in tmp if x.strip()]
    tmp2 = []
    for line in tmp:
        mdata = dict(line=line)
        line = line.split(' on ')
        name = line.pop(0)
        line = ''.join(line)
        line = line.split(' type ')
        mount_point = line.pop(0)
        mdata.update(name=name, mount_point=mount_point)
        tmp2.append(mdata)
    return tmp2


def summarize_fpath(fpath):
    """ truncates a filepath to be more suitable for display.
        every instance of $HOME is replaced with ~
    """
    if home():
        return fpath.replace(home(), '~')
