'''This script purges all jobs from a Perforce server, removing fix
records if there is any.

$Author: lester_cheung $
$Id: //guest/lester_cheung/p4util/p4util/adm/rmjobs.py#1 $

'''

__version__ = '0.{0}'.format('$Change: 15148 $'.split()[-2])

import argparse
import sys
import logging
logging.basicConfig(format='%(asctime)-15s %(funcName)s.%(levelname)s %(message)s',
                    level=logging.DEBUG)

from ..p4cli import P4


def parse_args():
    ap = argparse.ArgumentParser(description='MYPROG')
    p4 = P4()
    ap.add_argument('-p', '--port', metavar=p4.env('P4PORT'), default=p4.env('P4PORT'))
    ap.add_argument('-u', '--user', metavar=p4.env('P4USER'), default=p4.env('P4USER'))
    ap.add_argument('-c', '--client', metavar=p4.env('P4CLIENT'), default=p4.env('P4CLIENT'))
    ap.add_argument('-C', '--charset', metavar=p4.env('P4CHARSET'), default=p4.env('P4CHARSET'))
    ap.add_argument('-y', '--do-it', action='store_true', default=False)
    return ap.parse_args()

def main():
    log = logging.getLogger(__name__)
    cfg = parse_args()
    log.debug(cfg)
    p4 = P4()
    p4.prog = __file__

    if cfg.user:
        p4.user = cfg.user
    if cfg.port:
        p4.port = cfg.port
    if cfg.client:
        p4.client = cfg.client
    if cfg.charset:
        p4.charset = cfg.charset

    p4.connect()

    ## YOUR PROG HERE
    from pprint import pformat, pprint
    import shlex

    log.info(pformat(p4.run_info()))

    for job in p4.run_jobs():
        jobname = job['Job']
        for fix in p4.run_fixes(['-j', jobname]):
            chgno = fix.get('Change')
            if cfg.do_it:
                log.info(p4.run_fix(shlex.split('-d -c {chg} {job}'.format(chg=chgno, job=jobname))))
            else:
                log.info('Would remove fix record {}->{} with -y'.format(chgno, jobname))
        if cfg.do_it:
            log.info(p4.run_job(shlex.split('-d {job}'.format(job=jobname))))
        else:
            log.info('Would remove {} with -y'.format(jobname))
    p4.disconnect()

if __name__ == '__main__':
    main()
