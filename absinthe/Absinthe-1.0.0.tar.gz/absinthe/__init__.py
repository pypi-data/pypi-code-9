import os
import shutil

from .tools.utils import Storage

dirs = Storage(
    package_path = os.path.abspath(os.path.dirname(__file__)),
    data_dir = os.path.join(os.path.expanduser('~'), '.absinthe'),
)

dirs.update(Storage(
    server_listener = os.path.join(dirs.package_path, 'server_listen.py'),
    config_file = os.path.join(dirs.data_dir, 'config.json'),
))

def init_data_dir():
    if not os.path.isdir(dirs.data_dir):
        os.mkdir(dirs.data_dir)

    if not os.path.isfile(dirs.config_file):
        shutil.copyfile(os.path.join(dirs.package_path, 'config_example.json'), dirs.config_file)
