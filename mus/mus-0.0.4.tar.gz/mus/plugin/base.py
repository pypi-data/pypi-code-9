
from datetime import datetime
import os
import socket
import uuid

import colored as col
from dateutil.tz import tzlocal
import leip
from path import Path
import pytz

import mus.mongo


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
    for t in trecs:
        if t['task'] != rec.get('task'): continue
        timepoints.append(t['time'])
        if not t.get('event'): continue
        code = e2c[t['event']]
        if t['_id'] == rec['_id']:
            rv.extend([col.bg(208), col.fg(0)])
        else:
            rv.extend([col.bg(242), col.fg(0)])

        rv.extend([code, col.attr(0)])
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
        (10, "red"),
        (50, "deep_pink_4c"),
        (75, 103),
        (101, 0)]

    for l, c in level_color:
        levelcolor = 'green'
        if rec['level'] <= l:
            levelcolor = c
            break

    # level indicator
    rv = [col.fg('white'),
          col.bg(levelcolor),
          "%2d" % min(99, rec['level']),
          col.attr(0)]
    rvu = [ "%2d" % min(99, rec['level']) ]

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
    if not rec['channel'] == 'default':
        rv.extend([" ", col.fg(62),
                   rec['channel'], col.attr(0)])
        rvu.extend([" ", rec['channel']])

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
@leip.arg('-t', '--task', help='regarding a certain task (specify a unique id)')
@leip.flag('-T', '--random_task', help='as -t, but assign & return a random task id')
@leip.arg('-e', '--event', help='unique event within this task')
@leip.command
def log(app, args):
    """
    Log a message
    """
    db = mus.mongo.get_message_db(app)
    record = {}
    record['time'] = datetime.utcnow()
    record['host'] = socket.gethostname()
    if args.random_task:
        taskid = uuid.uuid4()
        record['task'] = taskid
    elif args.task:
        record['task'] = args.task
    if args.event:
        if not args.event in app.conf['allowed_events']:
            lg.critical("event %s is not allowed" % args.event)
        record['event'] = args.event
    record['cwd'] = Path(os.getcwd()).expanduser().expand()
    if args.message:
        record['message'] = " ".join(args.message)
    channel = args.channel if not args.channel is None else "default"
    record['channel'] = channel
    record['level'] = args.level
    db.insert_one(record)
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


@leip.arg('no', default=10, nargs='?', type=int, help='no records to show')
@leip.flag('-f', '--follow', help='as tail -f')
@leip.arg('-l', '--level', type=int, help='error level cutoff - show only errors ' +
          'with a level below this', default=100)
@leip.flag('-e', '--event_view')
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

    def gettasks(tids):
        query = {"task": {"$in": list(tids)}}
        tres = list(db.find(query).sort('time'))
        return(tres)

    if not args.follow:
        # just print 10 last records & exit
        results = list(reversed(list(db.find(query).sort('time', -1).limit(args.no))))
        tids = set([x['task'] for x in results if x.get('task')])
        trecs = gettasks(tids)
        print
        for rec in results:
            _recprint(rec, trecs)
