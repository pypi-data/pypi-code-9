#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''A script to (one-way) copy jobs from one Perforce server to
another.

Configure the script using the command line options or using a
INI-styled file and pass it in using the -c option.

An config file would be similar to:

  [job-replicator]
  src_p4port = P4PORT0:1666
  src_p4user = P4USER
  # P4CHARSET - none, utf8, auto etc.
  src_p4charset = none


  dst_p4port = P4PORT1:1666
  dst_p4user = P4USER
  dst_p4charset = none

  label_mappings= {
      "Project": {"newlabel": "Product", "default": "workshop",
          		    "transformation": [
          		    ["perforce_software-(?P<proj>.*)", "\\g<proj>"],
          		    ["perforce-software-(?P<proj>.*)", "\\g<proj>"],
          		    ["ProjectA", "ProductA"]] },
          }

  states = p4://P4USER@P4PORT/jobxfr.P4PORT0
  states_p4charset = none


src_* and dst_* specifies the connection details of the source
and destination servers respectively.

"label_mappings" is for you to:

1. Map fields with different names together (newlabel).

2. Rename field values (transformation).

3. Set default values (default).



@p4lester

'''
from __future__ import print_function

import P4
import argparse
import atexit
import json
import logging
import os
import re
import sys
import traceback

from pprint import pprint, pformat
from datetime import datetime

PY2 = False
if sys.version_info.major < 3:
    PY2 = True
    from ConfigParser import SafeConfigParser as configparser
    from urlparse import urlparse
else:
    from configparser import ConfigParser as configparser
    from urllib.parse import urlparse

DEFAULTS = dict(
    src_p4port    = 'perforce:1666',
    src_p4user    = 'perforce',
    src_p4charset = 'auto',
    dst_p4port    = 'perforce:1667',
    dst_p4user    = 'perforce',
    dst_p4charset = 'auto',
    label_mappings = {},

    states   = 'states.json',
    states_p4charset = 'none',
)


def parse_args():
    cfg = {}

    ap0 = argparse.ArgumentParser(add_help=False)  # turn off help
    ap0.add_argument('-c', '--config-file')
    args0, remaining_args = ap0.parse_known_args()

    if args0.config_file:
        confp = configparser()
        confp.read([args0.config_file])
        cfg = dict(confp.items('job-replicator'))

        for key in cfg:
            DEFAULTS[key] = cfg[key]

    ap1 = argparse.ArgumentParser(
        description='Replicate Perforce jobs from one server to another',
        parents=[ap0],          # so we know about their options
        epilog='Share & enjoy! https://twitter.com/p4lester'
    )

    ap1.add_argument('--src-p4port', metavar=DEFAULTS.get('src_p4port'))
    ap1.add_argument('--src-p4user', metavar=DEFAULTS.get('src_p4user'))
    ap1.add_argument('--src-p4charset', metavar=DEFAULTS.get('src_p4charset'))
    ap1.add_argument('--src-swarm-url', metavar='https://swarm.example.org/')
    ap1.add_argument('--dst-p4port', metavar=DEFAULTS.get('src_p4port'))
    ap1.add_argument('--dst-p4user', metavar=DEFAULTS.get('src_p4user'))
    ap1.add_argument('--dst-p4charset', metavar=DEFAULTS.get('src_p4charset'))

    ap1.add_argument('--states', metavar=DEFAULTS.get('states'),
                     help='path to a file or an URL in the "p4://P4PORT/key" format')
    ap1.add_argument('--states_p4charset', metavar='<file>|p4://user@p4port/key',
                     help='ignored if --states starts with "p4://"')
    ap1.add_argument('--label-mappings', type=json.loads,
                     help='{"OrgLabelName": {"newlabel": "NewLabelName", "transformation":'
                     ' [[regex0, regex1], ...]}}')

    ap1.add_argument('queries', nargs='*')

    ap1.set_defaults(**DEFAULTS)
    args1 = ap1.parse_args(remaining_args)
    args1.config_file = args0.config_file
    return args1

class P4JobRepl(object):
    '''Replicate jobs from one Perforce server to another.'''

    def __init__(self, cfg):
        # lookup dictionary used in replicate()
        self.label_dst2src = dict([ (x[1].get('newlabel'), x[0])
                                    for x in cfg.label_mappings.items() ])
        self.cfg = cfg

        self.log = logging.getLogger('JobRepl')
        self.log.debug(pformat(cfg))

        self.p4states = None
        self.load_states()
        self.log.debug(self.states)

        # Setup P4 connections
        self.src, self.dst = P4.P4(), P4.P4()
        src, dst = self.src, self.dst  # less typing...

        src.port = cfg.src_p4port
        dst.port = cfg.dst_p4port

        src.user = cfg.src_p4user
        dst.user = cfg.dst_p4user

        src.prog = dst.prog = 'P4JobRepl'

        src.charset = cfg.src_p4charset
        dst.charset = cfg.dst_p4charset

        src.connect()
        dst.connect()

        # jobspec
        self.dst_jobspec = dst.run_jobspec('-o')[0]

        ## voodoo starts: this simply gets the required fields from dst_jobspec
        from operator import itemgetter
        self.dst_required_labels = list( map( itemgetter(1), \
            filter ( lambda y: y[-1] == 'required', \
                [x.split() for x in self.dst_jobspec['Fields']] ) ) )
        ## voodoo ends

        # accepted values
        self.dst_values = dict([ x.split() for x in self.dst_jobspec['Values'] ])
        self.dst_presets = dict([x.split(' ', 1) for x in self.dst_jobspec.get('Presets')])

        # clean up on exit
        atexit.register(self.cleanup)

    def cleanup(self):
        '''Good boys clean up after themselves... '''
        self.log.info('cleaning up...')
        self.src.disconnect()
        self.dst.disconnect()
        if self.cfg.states.startswith('p4://'):
            if self.p4states:
                self.p4states.disconnect()
        else:
            with open(self.cfg.states, 'w') as fd:
                json.dump(self.states, fd)

    def main(self):
        for q in self.cfg.queries:
            for job in self.src.run_jobs(['-e', q]):
                if job['Job'] in self.states.get('map', {}):
                    self.log.debug('skipping {}'.format(job['Job']))
                    continue
                self.replicate(job)

    def replicate(self, job0):

        job1 = self.dst.fetch_job()
        undefined = {}
        log = self.log

        # copy values from job0 to job1, transforming values as configured
        for label in job0:
            value = job0[label].strip()
            if not value:       # skip if we have an empty value
                continue
            newlabel = self.cfg.label_mappings.get(label, {}).get('newlabel', label)

            for regex0, regex1 in self.cfg.label_mappings.get(label, {}).get('transformation', []):
                log.debug('RE: {}, {} => {}'.format(value, regex0, regex1))
                value = re.sub(regex0, regex1, value)

            try:
                if newlabel in job1:
                    job1[newlabel] = str(value) # unicode->str for PY2
                else:
                    undefined[newlabel] = str(value)
            except Exception as e:
                traceback.print_exc()
                log.info("{}->{}".format(label, value))
                log.error(newlabel)
                log.error(job1.keys())
                raise e

        job1['Job'] = 'new'   # we want to create a new job

        # stuff undefined labels at the end of the description
        extra_desc = []
        for label, value in undefined.items():
            extra_desc.append('{label}: {value}'.format(label=label, value=value))
        job1['Description'] = job1['Description'].strip() + '\n\n' + '\n'.join(extra_desc)

        job0ref = '{src} ({job0name})'.format(src=self.src.port,
                                              job0name=job0['Job'])
        if self.cfg.src_swarm_url:
            job0ref = '{url}/{job0name}'.format(url=self.cfg.src_swarm_url.rstrip('/'),
                                                job0name=job0['Job'])

        notes = '''\n\nJobXfr replicated this from {job0ref} on {dt}.'''.format(
            job0ref=job0ref,
            dt=datetime.now().strftime('%Y/%m/%d %H:%M:%S'))

        job1['Description'] = job1['Description'].strip() + notes


        # Use default if value is not defined or not a valid value
        for label in self.dst_required_labels:
            val          = job1.get(label)
            valid_values = self.dst_values.get(label)
            src_label    = self.label_dst2src.get(label) # oldlabel
            default_val  = self.cfg.label_mappings.get(src_label, {}).get('default') or \
                           self.dst_presets.get(src_label)
            if not val or valid_values and val not in valid_values:
                val = default_val

            if not val:
                log.warn('skipping required field {} => {}'.format(label, val))
                log.debug('default from mapping => {}  preset from dst jobspec => {}'.format(
                    self.cfg.label_mappings.get(src_label, {}).get('default'),
                    self.dst_presets.get(src_label)))
                continue

            if PY2 and type(val) == unicode:
                val = val.encode('utf8', 'replace')
            job1[label] = val

        log.debug(job1)
        self.dst.input = job1
        rv = self.dst.run_job('-i')
        try:
            job1name = rv[0].split()[1]
        except:
            log.error(rv)
            return

        log.debug('dst => {}'.format(job1))
        log.info('{} => {}'.format(job0['Job'], job1name))

        # Save the mappings for later use.
        mapping = self.states.get('map', {})
        mapping[job0['Job']] = job1name
        self.states['map'] = mapping

        # flush to disk in case we fail in the jobs that follows
        self.save_states()

    def save_states(self):
        if self.cfg.states.startswith('p4://'):
            u = urlparse(self.cfg.states)
            if not self.p4states or not self.p4states.connected():
                self.log.warn('creating a new instnace of p4!')
                p4 = P4.P4()
                uu = u.netloc.split('@')
                if len(uu) == 2:
                    p4.user, p4.port = uu
                else:
                    assert len(uu) == 1
                    p4.port = uu[0]
                p4.charset = self.cfg.states_p4charset
                p4.connect()
                self.p4states = p4
            key = u.path.lstrip('/')
            val = json.dumps(self.states)
            rv = self.p4states.run_key(key, val)
            # self.log.debug(rv)
        else:
            with open(self.cfg.states, 'w') as fd:
                json.dump(self.states, fd)

    def load_states(self):
        '''load states from files or from a p4 key'''
        if self.cfg.states.startswith('p4://'):
            p4 = P4.P4()
            u = urlparse(self.cfg.states)
            uu = u.netloc.split('@')
            if len(uu) == 2:
                p4.user, p4.port = uu
            else:
                assert len(uu) == 1
                p4.port = uu[0]
            p4.charset = self.cfg.states_p4charset
            key = u.path.lstrip('/')
            p4.connect()
            self.states = json.loads(p4.run_key(key)[0]['value'])
            if self.states == 0:
                self.states = {}
            self.p4states = p4 # so we don't have to reconnect to save the states
        elif os.path.exists(self.cfg.states):
            with open(self.cfg.states) as fd:
                self.states = json.load(fd)
        else:
            self.states = {}

        return self.states

    def requried_labels(self, jobspec):
        labels = []
        for fid, fname, dtype, flen, ftype in [ x.split() for x in jobspec['Fields'] ]:
            labels.append(fname)
        return labels

if __name__ == '__main__':
    cfg = parse_args()
    debuglvl = logging.INFO
    debuglvl = logging.DEBUG
    formatstr = '%(asctime)s %(message)s'
    logging.basicConfig(level=debuglvl, format=formatstr)

    repl = P4JobRepl(cfg)
    repl.main()
