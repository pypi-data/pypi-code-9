import argparse
import hashlib
import os
import sys
import subprocess
import time
import threading
import watchdog
import watchdog.events
import watchdog.observers
from reseasdk.run import run_emulator
from reseasdk.helpers import info, notice, error, \
    dict_to_strdict
from reseasdk.commands.build import build


SHORT_HELP = "build and run tests"
LONG_HELP = """
Usage: reseasdk test
"""


def test(args):
    cs = build(args)
    defaults = cs['defaults']

    info('ReseaSDK: build finished successfully, starting the executable...')
    env = dict_to_strdict(defaults)
    cmd = [defaults['HAL_RUN'], defaults['BUILD_DIR'] + '/application']
    run_emulator(cmd, save_log='build/{}/boot.log'.format(args['target']),
                 env=env, test=True)


class FSEventHandler(watchdog.events.FileSystemEventHandler):

    def __init__(self):
        super().__init__()
        self.lock = threading.Lock()
        self.last_file = ''
        self.last_hash = ''

    def on_any_event(self, event):
        def run_test():
            argv = list(filter(lambda x: x != '-P', sys.argv))
            subprocess.Popen(argv).wait()
            info('ReseaSDK: watching changes (Ctrl-D to quit)')

        def is_target_ext(path):
            exts = [
                'c', 'h', 'S',
                'yml',
                'ld',
                'cfg',
                'sh', 'py'
            ]
            return os.path.splitext(path)[1].lstrip('.') in exts

        with self.lock:
            # ignore directory changes
            if not os.path.isdir(event.src_path):
                # XXX: exclude files in the build directory
                if '/build/test/' in event.src_path:
                    return

                try:
                    with open(event.src_path, 'rb') as f:
                        hash = hashlib.sha1(f.read()).hexdigest()
                except:
                    # the file may be deleted (e.g. Emacs backup files)
                    return

                path = os.path.basename(event.src_path)

                if (is_target_ext(path) and
                   (self.last_hash != hash or self.last_file != path)):
                    self.last_hash = hash
                    self.last_file = path
                    info('ReseaSDK: detected changes in files'
                         '-- starting a test')
                    threading.Thread(target=run_test, daemon=True).start()


def main(args_):
    parser = argparse.ArgumentParser(prog='reseasdk test',
                                     description='test an executable')
    parser.add_argument('-r', action='store_true',
                        help='rebuild the executable')
    parser.add_argument('-P', action='store_true',
                        help='run tests automatically when'
                             'it detect a changes in files')
    parser.add_argument('--target', default='test', help='the build target')
    parser.add_argument('--dump', action='store_true',
                        help='dump generated files for debugging')
    parser.add_argument('--no-prettify', action='store_true',
                        help="don't prettify output")
    parser.add_argument('--all-in-one', action='store_true',
                        help='embed all required applications so that'
                             'discovery() always succeed')
    parser.add_argument('--single-app', action='store_true',
                        help='no threading')
    parser.add_argument('defaults', nargs='*',
                        help='default variables (FOO=bar)')

    args = vars(parser.parse_args(args_))
    args['defaults'].append('TEST=yes')

    if args['P']:
        # look for .git
        cwd = os.getcwd()
        while os.getcwd() != '/':
            if os.path.exists('.git'):
                path = os.getcwd()
            os.chdir('..')
        if os.getcwd() != '/':
            path = os.getcwd()
        os.chdir(cwd)

        info('ReseaSDK: watching changes in {} (Ctrl-D to quit)'.format(path))
        observer = watchdog.observers.Observer()
        observer.schedule(FSEventHandler(), path, recursive=True)
        observer.daemon = True
        observer.start()
        try:
            sys.stdin.read(1)
        except KeyboardInterrupt:
            pass

        info('ReseaSDK: stopping')
        observer.stop()
        observer.join()
    else:
        test(args)
