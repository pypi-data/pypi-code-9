import ohh
import sys
import getpass
import os
import requests
import json
import dateutil.parser
from dateutil.tz import tzlocal
import psutil
from ohh.background_runner import BackgroundRunner
import ohh.shell_completion
from datetime import datetime
try:
    from configparser import ConfigParser
except ImportError:
    from ConfigParser import ConfigParser


class Runner(object):
    def __init__(self, basedir='~/.ohh'):
        super(Runner, self).__init__()
        self._basedir = os.path.expanduser(basedir)

        if not os.path.isdir(self._basedir):
            os.mkdir(self._basedir)

        self._log_file = os.path.join(self._basedir, 'ohh.log')
        self._pid_file = os.path.join(self._basedir, 'ohh.pid')
        self._config_file = os.path.join(self._basedir, 'ohhrc')

        self.config = ConfigParser()
        self._read_config()
        self._background_runner = BackgroundRunner(
            self._pid_file, stdout=self._log_file, stderr=self._log_file)

    def _read_input(self):
        python_version = sys.version_info.major
        if python_version == 3:
            return input()
        else:
            return raw_input()

    def _create_config(self):
        self.config.add_section('ohh')
        for k, v in ohh.DEFAULT_CONFIG.items():
            self.config.set('ohh', k, v)
        self._save_config()

    def _read_config(self):
        if not os.path.isfile(self._config_file):
            self._create_config()
        else:
            self.config.read(self._config_file)

    def _get_request_info(self, path):
        headers = {}
        base_url = self.config.get('ohh', 'endpoint')
        url = os.path.join(base_url, path)
        token = self.config.get('ohh', 'token')
        if token:
            headers['X-Token'] = token
        return url, headers

    def _get(self, path, params):
        url, headers = self._get_request_info(path)
        return requests.get(url, headers=headers, params=params)

    def _post(self, path, data=None):
        url, headers = self._get_request_info(path)
        if data:
            data = json.dumps(data)
            headers['Content-Type'] = 'application/json'
        return requests.post(url, data=data, headers=headers)

    def login(self):
        sys.stdout.write('Email: ')
        email = self._read_input()
        password = getpass.getpass()
        r = self._post('authenticate', {'mail': email, 'password': password})
        if r.status_code == 401:
            raise ohh.OhhError('wrong email or password')
        self._check_http_status('login', r.status_code)
        self.config.set('ohh', 'token', r.json()['token'])
        self._save_config()

    def _save_config(self):
        with open(self._config_file, 'w') as f:
            self.config.write(f)

    def start(self, start_daemon=True, foreground=False, session_type='computer'):
        info = self.get_session_info(session_type)
        if info and info['active']:
            if session_type == 'computer':
                print("session already started, use 'ohh stop' to stop")
            else:
                print("already at work, use 'ohh stop --office' to stop")
        else:
            self._check_credentials()
            r = self._post('sessions/start', data={'session_type': session_type})
            self._check_http_status('start', r.status_code)
        if start_daemon and not self.is_running() and session_type == 'computer':
            print('ohh is now running')
            self._clean_pid_file()
            if foreground:
                self._background_runner.run(self, self._basedir)
            else:
                self._background_runner.start(self, self._basedir)

    def stop(self, kill_daemon=True, session_type='computer'):
        info = self.get_session_info(session_type)
        if info and info['status'] == 'idle':
            if session_type == 'computer':
                print("session already stopped, use 'ohh start' to start one")
            else:
                print("already stopped work, use 'ohh start --office' to start")
        else:
            self._check_credentials()
            r = self._post('sessions/end', data={'session_type': session_type})
            self._check_http_status('stop', r.status_code)
        if kill_daemon and self.is_running() and session_type == 'computer':
            self._background_runner.stop()
            print('ohh has stopped')

    def _clean_pid_file(self):
        pid = self._background_runner.get_pid()
        if pid and not psutil.pid_exists(pid):
            os.unlink(self._pid_file)

    def is_running(self):
        pid = self._background_runner.get_pid()
        return pid and psutil.pid_exists(pid)

    def _check_http_status(self, action, status_code):
        if status_code != 200:
            msg = 'failed to {0}, got status {1}'
            raise ohh.OhhError(msg.format(action, status_code))

    def status(self):
        if self.is_running():
            pid = self._background_runner.get_pid()
            print('ohh is running (pid {0})'.format(pid))
        else:
            print('ohh is not running')
        self.show_info()
        self.show_info('office')

    def get_session_info(self, session_type='computer'):
        r = self._get('sessions/last', params={'session_type': session_type})
        if r.status_code != 200:
            return False
        session = r.json()
        if session_type == 'computer':
            status, time = ['idle', 'end_time'] if session['done'] else ['active', 'start_time']
        else:
            status, time = ['out of work', 'end_time'] if session['done'] else ['at work', 'start_time']
        return {'time': dateutil.parser.parse(session[time]), 'status': status, 'active': not session['done']}

    def show_info(self, session_type='computer'):
        info = self.get_session_info(session_type)
        if info:
            timediff = self._timediff(info['time'])
            print("You have been {0} for {1}.".format(info['status'], timediff))

    def _check_credentials(self):
        token = self.config.get('ohh', 'token')
        if token is None or token == 'None':
            raise ohh.OhhError("Please run 'ohh login'")

    def _timediff(self, start_time):
        s = (datetime.now(tzlocal()) - start_time).seconds
        if s < 60:
            return '{0} seconds'.format(s)
        elif s < 3600:
            return '{0} minutes and {1} seconds'.format(s // 60, s % 60)
        else:
            return '{0} hours and {1} minutes'.format(s // 3600, s // 60 % 60)

    def setup_shell(self):
        current_shell = os.environ.get('SHELL')
        if not current_shell:
            print('could not find your current shell, aborting')
        elif current_shell.endswith('zsh'):
            self.setup_zsh()
        else:
            print('sorry, {0} is not supported yet'.format(current_shell))

    def setup_zsh(self):
        zsh_dir = os.path.join(self._basedir, 'zsh')
        completion_dir = os.path.join(zsh_dir, 'completions')
        if not os.path.isdir(zsh_dir):
            os.mkdir(zsh_dir)
        if not os.path.isdir(completion_dir):
            os.mkdir(completion_dir)
        with open(os.path.join(zsh_dir, 'ohh-init.sh'), 'w') as f:
            f.write(ohh.shell_completion.INIT_FILE)
        with open(os.path.join(completion_dir, '_ohh'), 'w') as f:
            f.write(ohh.shell_completion.COMPLETION_FILE)
        self._append_zshrc()

    def _append_zshrc(self):
        zshrc = os.path.expanduser('~/.zshrc')
        with open(zshrc, 'r') as f:
            contains_initialization = 'ohh-init' in f.read()
        if not contains_initialization:
            with open(zshrc, 'a') as f:
                f.write(ohh.shell_completion.INIT_CONTENT)
            print('your zshrc has been appended, restart your shell')
        else:
            print('everything should be working, try restarting your shell if it is not')

    def run(self, action, *args, **kwargs):
        return getattr(self, action)(*args, **kwargs)
