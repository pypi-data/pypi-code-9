from ohh.daemon import Daemon
import signal
import psutil
from os.path import join
import sys
import collections
import logging
import json
import sys
from datetime import datetime
from logging.handlers import RotatingFileHandler

if sys.platform == 'darwin':
    from pync import Notifier
else:
    import subprocess


LOG_FORMAT = '%(asctime)-15s %(message)s'


class BackgroundRunner(Daemon):
    def run(self, runner, basedir):
        self._make_logger(basedir)
        self._basedir = basedir
        self._status = 'active'
        self._runner = runner
        self._usage_data = collections.deque(maxlen=60*5)
        signal.signal(signal.SIGINT, self._handle_stop)
        self._logger.info('ohh has started')
        counter = 0
        self._last_change_time = datetime.now()
        self._last_ping = datetime.now()
        while True:
            try:
                self.main_loop(counter == 0)
            except Exception as e:
                self._logger.warning('an error occured in main loop: {0}'.format(str(e)))
            counter = (counter + 1) % 10

    def main_loop(self, should_ping):
        cpu_usage = psutil.cpu_percent(interval=1)
        self._usage_data.append(cpu_usage)
        idle = self._is_idle()
        no_ping = (datetime.now() - self._last_ping).total_seconds() > 60 * 5
        time_diff_large_enough = (datetime.now() - self._last_change_time).total_seconds() > 60
        if (idle or no_ping) and self._status == 'active' and time_diff_large_enough:
            self._change_status('idle')
        elif not idle and self._status == 'idle':
            self._change_status('active')
        if should_ping and self._status == 'active':
            r = self._runner._post('sessions/ping')
            if r.status_code != 204:
                self._logger.warning('failed to ping, got {0}'.format(r.status_code))
            self._last_ping = datetime.now()

    def _make_logger(self, basedir):
        logfile = join(basedir, 'ohh.log')
        self._logger = logging.getLogger('ohh')
        handler = RotatingFileHandler(logfile, maxBytes=1024**2)
        handler.setFormatter(logging.Formatter(fmt=LOG_FORMAT))
        self._logger.addHandler(handler)
        self._logger.setLevel(logging.INFO)

    def _change_status(self, status):
        try:
            self._change_server_status(status)
        except Exception as e:
            self._logger.error('could not update status: {0}'.format(str(e)))
            return
        self._status = status
        self._logger.info('status changed to {0}'.format(self._status))
        self._notify(status)
        self._last_change_time = datetime.now()

    def _change_server_status(self, status):
        if status == self._runner.get_session_info()['status']:
            return
        if status == 'active':
            self._runner.start(start_daemon=False)
        else:
            self._runner.stop(kill_daemon=False)

    def _notify(self, status):
        msg = 'OHH - You are now ' + status
        if sys.platform == 'darwin':
            Notifier.notify(msg)
        elif sys.platform.startswith('linux'):
            subprocess.Popen(['notify-send', msg])

    # TODO: tune logic
    def _is_idle(self):
        if len(self._usage_data) < 60*5:
            return False
        total = 0
        high_usages_count = 0
        for percent in self._usage_data:
            if percent > int(self._runner.config.get('ohh', 'cpu_threshold')):
                high_usages_count += 1
            total += percent
        return high_usages_count < 30

    def _handle_stop(self, signal, frame):
        self._runner.stop(kill_daemon=False)
        self._logger.info('ohh has stopped')
        sys.exit(0)

if __name__ == '__main__':
    from ohh.runner import Runner
    import os
    runner = Runner()
    bg_runner = BackgroundRunner('/tmp/ohh.pid')
    bg_runner.run(runner, os.path.expanduser('~/.ohh'))
    bg_runner._change_status('idle')
