from __future__ import absolute_import

import logging
import subprocess
import os
import time
import glob

class PsqlDumperManager:

    def __init__(self, conf, pg_user, dump_root, email=None, success=False):
        self.conf = conf
        self.pg_user = pg_user
        self.dump_root = dump_root
        if email:
            self.notify = True
            self.email = email
            self.notify_success = success
        else:
            self.notify = False

    def check_if_master(self):
        try:
            subprocess.check_call("/usr/bin/psql -U {} -t -P format=unaligned -c 'SELECT pg_is_in_recovery();' | grep -q 'f'".format(self.pg_user), shell = True)
            return True
        except subprocess.CalledProcessError:
            return False

    def __db_exists(self, db):
        try:
            subprocess.check_call('/usr/bin/psql -U {} -lqt | cut -d \| -f 1 | grep -w {} > /dev/null'.format(self.pg_user, db), shell = True)
            return True
        except subprocess.CalledProcessError:
            return False

    def select_databases(self):
        for db in self.conf.keys():
            if self.__db_exists(db):
                now = int(time.strftime("%H"))
                freq = int(self.conf[db]['frequency'])
                if now % freq == 0:
                    dump_ext = 'sql' if self.conf[db]['sql_dump'] else 'dmp'
                    dump_args = '' if self.conf[db]['sql_dump'] else ' -Fc -b'

                    self.conf[db]['dump'] = True
                    self.conf[db]['dump_cmd'] = '/usr/bin/pg_dump -U {user}{args} {db} > {root}/{db}_DATE.{ext}'.format(user=self.pg_user, args=dump_args, db=db, root=self.dump_root, ext=dump_ext)
                else:
                    self.conf[db]['dump'] = False
                    self.conf[db]['details'] = 'Not time to backup yet (every {} hours)'.format(self.conf[db]['frequency'])
            else:
                self.conf[db]['dump'] = False
                self.conf[db]['details'] = 'Database does not exist on this server'

    def run_jobs(self):
        for db in self.conf.keys():
            date = time.strftime("%Y%m%d-%H%M%S")

            if self.conf[db]['dump']:
                try:
                    logging.getLogger('psqldumper').info('[{}] Running dump job'.format(db))

                    cmd = '{} 2> {}/{}_{}.log'.format(self.conf[db]['dump_cmd'].replace('DATE',date), self.dump_root, db, date)
                    subprocess.check_call(cmd, shell = True)
                    
                    logging.getLogger('psqldumper').info('[{}] Dump job completed'.format(db))
                    self.conf[db]['status'] = 'Done'

                    logging.getLogger('psqldumper').info('[{}] Cleaning up old dump'.format(db))

                    retention = int(self.conf[db]['retention'])
                    now = time.time()
                    cutoff = now - (retention * 86400)
                    glob_match = '{}/{}_*'.format(self.dump_root, db)
                    for dump in glob.glob(glob_match):
                        c = os.stat(dump).st_ctime
                        if c < cutoff:
                            logging.getLogger('psqldumper').info('[{}] Removing old dump: {}'.format(db, dump))
                            os.remove(dump)
                        else:
                            logging.getLogger('psqldumper').info('[{}] Not touching: {}'.format(db, dump))

                    logging.getLogger('psqldumper').info('[{}] Cleanup done'.format(db))
                except subprocess.CalledProcessError(e):
                    logging.getLogger('psqldumper').info('[{}] Dump job FAILED : {}'.format(db,e))
                    self.conf[db]['status'] = 'Failed'
                    self.conf[db]['details'] = 'Log file is attached'
                    self.conf[db]['logfile'] = '{}_{}.log'.format(db, date)
            else:
                logging.getLogger('psqldumper').info('[{}] Database dump ignored: {}'.format(db, self.conf[db]['details']))
                self.conf[db]['status'] = 'Ignored'

    def send_notifications(self):
        pass
