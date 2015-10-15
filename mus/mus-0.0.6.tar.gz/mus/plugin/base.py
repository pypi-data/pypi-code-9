
from datetime import datetime
from hashlib import md5
import logging
import os
import random
import socket
import time
import uuid

import colored as col
import coloredlogs
from dateutil.tz import tzlocal
import leip
from path import Path
import pytz

import mus.mongo

lg = logging.getLogger(__name__)


TASK_COLOR = {}

def event_format(rec, trecs):

    e2c = {'start': 's',
           'pause': 'p',
           'checkpoint': 'c',
           'queue': 'q',
           'finish': 'f',
           'error': 'e' }

    rv = ["|"]
    rvu = ["|"]

    timepoints = []

    if not rec.get('task'): return '', ''
    okrecs = []
    for t in trecs:
        if t['task'] != rec.get('task'): continue
        timepoints.append(t['time'])
        if not t.get('event'):
            continue
        okrecs.append(t)

    for t in okrecs:
        code = e2c[t['event']]
        if t['_id'] == rec['_id']:
            rv.extend([col.bg(208), col.fg(0), code, col.attr(0)])
            rvu.append(code)
            in_skipped_part=False
        else:
            if len(okrecs) > 8 and code == 'c':
                pass
            else:
                rv.extend([col.bg(0), col.fg(242), code, col.attr(0)])
                rvu.append(code)


    t = sorted(timepoints)[0]
    diff = rec['time'] - t
    tots = diff.total_seconds()

    if tots > 86400:
        ts = '%dd' % int(tots / 86400)
    elif tots > 3600:
        ts = '%dh' % int(tots / 3600)
    elif tots > 60:
        ts = '%dm' % int(tots / 60)
    else:
        ts = '%ds' % int(tots)


    rv.extend(['|', ts])
    rvu.extend(['|', ts])

    return ''.join(rv), ''.join(rvu)

def _recprint(rec, trecs):

    level_color = [
        (10, "red", 0),
        (50, "deep_pink_4c", 0),
        (75, 0, 103),
        (101, 0, 246)]

    bgc, fgc = 245, 0
    for l, bgc, fgc in level_color:
        if rec['level'] <= l:
            break

    # level indicator
    rv = [col.fg(fgc),
          col.bg(bgc),
          "%2d" % min(99, rec['level']),
          col.attr(0)]
    rvu = [ "%2d" % min(99, rec['level']) ]

    # unique_task_id
    if 'task' in rec:
        tid = md5()
        tid.update(str(rec['task']).encode())
        tid = tid.hexdigest()
        if not tid in TASK_COLOR:
            TASK_COLOR[tid] = random.choice(range(18, 228))
        tcol = TASK_COLOR[tid]
        rv.extend([ '|', col.bg(tcol), col.fg(0),tid[:2], col.attr(0)])
        rvu.extend(['|', tid])


    _a, _b = event_format(rec, trecs)
    rv.append(_a); rvu.append(_b)

    # date & time
    #db contains utc - convert to local
    loctime = pytz.utc.localize(rec['time']).astimezone(tzlocal())
    if loctime.date() == datetime.today().date():
        tstr = loctime.strftime("%H:%M:%S")
    else:
        tstr = loctime.strftime("%d/%b/%Y %H:%M:%S")
    rv.extend([" ", col.fg('dark_green_sea'),
               tstr, col.attr(0)])
    rvu.extend([" ", tstr])

    # channel
    if not rec.get('channel') == 'default':
        rv.extend([" ", col.fg(62),
                   rec.get('channel', '-'), col.attr(0)])
        rvu.extend([" ", rec.get('channel', '-')])

    # host = rec.get('host', 'n.a.')
    if rec.get('host'):
        rv.extend([" ", col.fg('orchid'), rec['host'], col.attr(0)])
        rvu.extend([" ", rec['host']])

    tw = os.get_terminal_size().columns
    mw = tw - len("".join(rvu)) - 2

    message = rec.get('message')
    if message:
        if mw < 10:
            rv.extend(["\n     ", col.fg(242), message[:tw-6], col.attr(0)])
            rvu.extend(["\n     ", message[:tw-6]])
        else:
            rv.extend([" ", col.fg(242), message[:mw], col.attr(0)])
            rvu.extend([" ", message[:mw]])
    print("".join(rv))


@leip.arg('message', nargs='*', help='message')
@leip.arg('-l', '--level', help='level (0/severe - 100/trivial)', type=int, default=75)
@leip.arg('-c', '--channel', help='channel')
@leip.arg('-x', '--expected_frequency', help='expected task frequency for '+
          'this channel')
@leip.arg('-t', '--task', help='regarding a certain task (specify a unique id)')
@leip.flag('-T', '--random_task', help='as -t, but assign & return a random task id')
@leip.arg('-e', '--event', help='unique event within this task')
@leip.command
def log(app, args):
    """
    Log a message
    """
    db = mus.mongo.get_message_db(app)
    cdb = mus.mongo.get_channel_db(app)

    record = {}
    rectime = datetime.utcnow()
    record['time'] = rectime
    host = socket.gethostname()
    record['host'] = host
    if args.random_task:
        taskid = str(uuid.uuid4())
        record['task'] = taskid
    elif args.task:
        record['task'] = args.task
        taskid = args.task
    else:
        taskid = "_notask"

    if args.event:
        event = args.event
        if not args.event in app.conf['allowed_events']:
            print("event %s is not allowed" % args.event)
            exit(-1)
        record['event'] = event
    else:
        event = '_noevent'

    record['cwd'] = Path(os.getcwd()).expanduser().expand()

    if args.message:
        record['message'] = " ".join(args.message)

    record['level'] = max(0, min(args.level, 100))

    channel = args.channel if not args.channel is None else "default"
    record['channel'] = args.channel
    new_rec_id = db.insert_one(record).inserted_id

    crec = cdb.find_one({'_id': channel})
    if crec is None:
        crec = {'_id': channel}
        cdb.insert_one(crec)
    update_field = {
        '$inc': {"counter.log": 1,
                 "counter.event.%s" % event: 1,
                 "counter.host.%s" % host: 1,
             },
        '$set': {"last_log_id": new_rec_id,
                 "last_time.log": rectime,
                 "last_time.event.%s" % event: rectime,
                 "last_time.host.%s" % host: rectime,
             },
    }
    #if args.event
    cdb.update({'_id': channel}, update_field)



    if args.random_task:
        print(taskid)

@leip.command
def create_indici(app, args):
    """
    Create the appropriate indici in mongodb
    """
    db = mus.mongo.get_message_db(app)
    for idx in app.conf['mongo_indici']:
        db.ensure_index(idx)


@leip.arg('channel')
@leip.command
def drop_channel(app, args):
    """
    Create the appropriate indici in mongodb
    """
    db = mus.mongo.get_message_db(app)
    cdb = mus.mongo.get_channel_db(app)

    lg.warning("dropping channel: %s", args.channel)

    db.remove(dict(channel=args.channel))
    cdb.remove(dict(_id=args.channel))

@leip.arg('task')
@leip.command
def drop_task(app, args):
    """
    Create the appropriate indici in mongodb
    """
    db = mus.mongo.get_message_db(app)
    lg.warning("dropping task: %s", args.task)
    db.remove(dict(task=args.task))


@leip.arg('no', default=10, nargs='?', type=int, help='no records to show')
@leip.arg('-c', '--channel')
@leip.flag('-f', '--follow', help='as tail -f')
@leip.arg('-l', '--level', type=int, help='error level cutoff - show only errors ' +
          'with a level below this', default=101)
@leip.flag('-e', '--event_view', help='show only events')
@leip.command
def tail(app, args):
    """
    show the most recent messages
    """
    db = mus.mongo.get_message_db(app)
    query = {}
    if args.event_view:
        query['event'] = {"$exists": True}
    if args.level:
        query['level'] = {"$lte": args.level}
    if args.channel:
        query['channel'] = args.channel

    def gettasks(tids):
        query = {"task": {"$in": list(tids)}}
        tres = list(db.find(query).sort('time'))
        return(tres)

    # just print 10 last records & exit
    results = list(reversed(list(db.find(query).sort('time', -1).limit(args.no))))
    tids = set([x['task'] for x in results if x.get('task')])
    trecs = gettasks(tids)

    if not args.follow:
        for rec in results:
            _recprint(rec, trecs)
        exit(0)


    # follow mode
    # first print
    for rec in results:
        _recprint(rec, trecs)

    # then loop & print new records
    most_recent_time = results[-1]['time']

    while True:
        query['time'] = {"$gt": most_recent_time}
        results = list(reversed(list(db.find(query).sort('time', -1).limit(args.no))))
        if len(results) > 0:
            tids = set([x['task'] for x in results if x.get('task')])
            trecs.extend(gettasks(tids))
            most_recent_time = results[-1]['time']
            for rec in results:
                _recprint(rec, trecs)
        time.sleep(1)
