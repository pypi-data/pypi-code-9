#!/usr/bin/env python

import matplotlib.pyplot   as plt
import pandas              as pd
import numpy               as np
import pprint              as pp

import radical.utils       as ru
import radical.pilot       as rp
import radical.pilot.utils as rpu
import os

import glob
import os

# "label", "component", "event", "message"
_prof_entries = [
    ('a_get_u',         'MainThread',       'get', 'MongoDB to Agent (PendingExecution)'),
    ('a_build_u',       'MainThread',       'Agent get unit meta', ''),
    ('a_mkdir_u',       'MainThread',       'Agent get unit mkdir', ''),
    ('a_notify_alloc',  'MainThread',       'put', 'Agent to update_queue (Allocating)'),
    ('a_to_s',          'MainThread',       'put', 'Agent to schedule_queue (Allocating)'),

    ('s_get_alloc',     'CONTINUOUS',       'get', 'schedule_queue to Scheduler (Allocating)'),
    ('s_alloc_failed',  'CONTINUOUS',       'schedule', 'allocation failed'),
    ('s_allocated',     'CONTINUOUS',       'schedule', 'allocated'),
    ('s_to_ewo',        'CONTINUOUS',       'put', 'Scheduler to execution_queue (Allocating)'),
    ('s_unqueue',       'CONTINUOUS',       'unqueue', 're-allocation done'),
  
    ('ewo_get',         'ExecWorker-',      'get', 'executing_queue to ExecutionWorker (Executing)'),
    ('ewo_launch',      'ExecWorker-',      'ExecWorker unit launch', ''),
    ('ewo_spawn',       'ExecWorker-',      'ExecWorker spawn', ''),
    ('ewo_script',      'ExecWorker-',      'launch script constructed', ''),
    ('ewo_pty',         'ExecWorker-',      'spawning passed to pty', ''),  
    ('ewo_notify_exec', 'ExecWorker-',      'put', 'ExecWorker to update_queue (Executing)'),
    ('ewo_to_ewa',      'ExecWorker-',      'put', 'ExecWorker to watcher (Executing)'),
  
    ('ewa_get',         'ExecWatcher-',     'get', 'ExecWatcher picked up unit'),
    ('ewa_complete',    'ExecWatcher-',     'execution complete', ''),
    ('ewa_notify_so',   'ExecWatcher-',     'put', 'ExecWatcher to update_queue (StagingOutput)'),
    ('ewa_to_sow',      'ExecWatcher-',     'put', 'ExecWatcher to stageout_queue (StagingOutput)'),
  
    ('sow_get_u',       'StageoutWorker-',  'get', 'stageout_queue to StageoutWorker (StagingOutput)'),
    ('sow_u_done',      'StageoutWorker-',  'final', 'stageout done'),
    ('sow_notify_done', 'StageoutWorker-',  'put', 'StageoutWorker to update_queue (Done)'),

    ('uw_get_alloc',    'UpdateWorker-',    'get', 'update_queue to UpdateWorker (Allocating)'),   
    ('uw_push_alloc',   'UpdateWorker-',    'unit update pushed (Allocating)', ''),
    ('uw_get_exec',     'UpdateWorker-',    'get', 'update_queue to UpdateWorker (Executing)'),
    ('uw_push_exec',    'UpdateWorker-',    'unit update pushed (Executing)', ''),
    ('uw_get_so',       'UpdateWorker-',    'get', 'update_queue to UpdateWorker (StagingOutput)'),
    ('uw_push_so',      'UpdateWorker-',    'unit update pushed (StagingOutput)', ''),
    ('uw_get_done',     'UpdateWorker-',    'get', 'update_queue to UpdateWorker (Done)'),
    ('uw_push_done',    'UpdateWorker-',    'unit update pushed (Done)', '')
]

# ------------------------------------------------------------------------------
#
prof  = "/home/merzky/saga/radical.pilot/rp.session.thinkie.merzky.016609.0007-pilot.0000.prof"
sid   = "rp.session.thinkie.merzky.016609.0007"
pid   = "pilot.0000"
frame = pd.read_csv(prof)

units = dict()
units['all']    = [x for x in frame.uid.dropna().unique() if x.startswith('unit')]
units['cloned'] = [x for x in units['all']                if 'clone' in x]
units['real']   = list(set(units['all']) - set(units['cloned']))

print "all    units : %5d" % len(units['all'])
print "real   units : %5d" % len(units['real'])
print "cloned units : %5d" % len(units['cloned'])

print frame

unit_data = list()

for uid in units['all'][:10]:
    
    print uid
    data = dict()
    tmp  = frame[(frame.uid == uid)]

    for t in _prof_entries:
        val = tmp[(tmp.component.str.startswith(t[1])) &
                  (tmp.event   == t[2]) &
                  (tmp.message == t[3])].time

        if len(val) == 1: data[t[0]] = val.values[0]
        else            : data[t[0]] = np.NaN

    unit_data.append (data)

unit_frame = pd.DataFrame(unit_data)
# print unit_frame

concurrency = list()
cu_num = 0
for index, row in frame.sort(columns=['time']).iterrows():

    if row.message == "ExecWorker to watcher (Executing)":
        cu_num += 1
        print row.time, cu_num
        concurrency.append ({'time': row.time, 'cu_num': cu_num})
    elif row.message == "execution complete":
        cu_num -= 1
        print row.time, cu_num
        concurrency.append ({'time': row.time, 'cu_num': cu_num})

conc_frame = pd.DataFrame (concurrency)
# print conc_frame

