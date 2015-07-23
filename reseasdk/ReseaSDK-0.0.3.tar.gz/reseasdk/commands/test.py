import argparse
import datetime
import os
import subprocess
from reseasdk.helpers import info, load_yaml
from reseasdk.commands.build import build, load_packages, dict_to_strdict


def main(args_):
    parser = argparse.ArgumentParser(prog='reseasdk test',
                                     description='test an executable')
    parser.add_argument('-r', action='store_true', help='rebuild the executable')
    args = parser.parse_args(args_)

    build('test', args.r)
    info('build has been successful, starting the executable...')

    # prepend a header to the log file
    with open('build/test/boot.log', 'a') as f:
        f.write('================ {} ================\n'.format(
                str(datetime.datetime.now())))

    # load build config
    config,_,_ = load_packages(load_yaml('package.yml'),
                               load_yaml('config.test.yml'), 'test')
    config['BUILD_DIR'] = 'build/test'

    # run test program speicified in HAL_TEST config
    cmd = '{} {}/executable 2>&1 |tee -a build/test/boot.log'.format(
              config['HAL_TEST'], config['BUILD_DIR'])
    subprocess.call(cmd, shell=True, env=dict_to_strdict(config))
