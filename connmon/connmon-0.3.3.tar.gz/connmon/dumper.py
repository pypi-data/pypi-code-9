import datetime
import time
import os

from zkcluster import util


class CSVDumper(object):
    def __init__(self, server):
        self.output_file = server.service_config['csv_dump']
        self.async_suite = server.async_suite
        self.stat = server.memos['stats']
        self.columns = server.service_config['csv_columns']
        self.token = server.service_config['csv_token']

        file_exists = os.access(self.output_file, os.F_OK)
        self.stream = open(self.output_file, 'w+')
        if not file_exists:
            self.stream.write(
                ",".join(self.columns) + "\n"
            )
            self.stream.flush()

        self.worker = self.async_suite.background_thread(self.dump)
        util.event_listen(self.stat, "message_received", self.message_received)
        self.last_updated = time.time()

    def message_received(self, message):
        self.last_updated = time.time()

    def dump(self):
        # TOOD: allow options for event-only dumping, formats besides
        # CSV(?), file rotation(?), per-server and per-process dumps
        # (e.g. not just per-application)
        last_written = time.time()
        while True:
            self.async_suite.sleep(1)
            if self.last_updated <= last_written:
                continue

            last_written = time.time()
            timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            hostprogs = list(self.stat.hostprogs.values())
            hostprogs.sort(
                key=lambda hostprog: (hostprog.hostname, hostprog.progname)
            )
            for hostprog in hostprogs:
                row = {
                    'timestamp': timestamp,
                    'token': self.token, 'hostname': hostprog.hostname,
                    'progname': hostprog.progname,
                    'process_count': hostprog.process_count,
                    'connection_count': hostprog.connection_count,
                    'max_process_count': hostprog.max_process_count,
                    'max_checkedout': hostprog.max_checkedout,
                    'max_connections': hostprog.max_connections,
                    'checkout_count': hostprog.checkout_count
                }

                self.stream.write(
                    ",".join(str(row.get(col)) for col in self.columns) + "\n"
                )
            self.stream.flush()
