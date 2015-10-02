
from datetime import datetime
import os
import socket

import colored as col
from dateutil.tz import tzlocal
import leip
from path import Path
import pytz

import mus.mongo


@leip.arg('message', nargs='*', help='message')
@leip.arg('-l', '--level', help='level (0/severe - 100/trivial)', type=int, default=75)
@leip.arg('-c', '--channel', help='channel')
@leip.command
def log(app, args):
    """
    Log a message
    """
    db = mus.mongo.get_message_db(app)
    record = {}
    record['time'] = datetime.utcnow()
    record['host'] = socket.gethostname()
    record['cwd'] = Path(os.getcwd()).expanduser().expand()
    record['message'] = " ".join(args.message)
    channel = args.channel if not args.channel is None else "default"
    record['channel'] = channel
    record['level'] = args.level
    db.insert_one(record)

@leip.command
def create_indici(app, args):
    """
    Create the appropriate indici in mongodb
    """
    db = mus.mongo.get_message_db(app)
    db.ensure_index('time')
    db.ensure_index('host')
    db.ensure_index('channel')
    db.ensure_index('level')
    db.ensure_index('cwd')


@leip.command
def tail(app, args):
    """
    show the most recent messages
    """
    db = mus.mongo.get_message_db(app)
    level_color = [
        (10, "red"),
        (50, "orange"),
        (75, "yellow")]

    def _recprint(rec):
        for l, c in level_color:
            color = 'green'
            if rec['level'] <= l:
                color = c
                break

        host = rec.get('host', 'n.a.')

        if rec['channel'] == 'default':
            chan = ""
        else:
            chan = " %s(%s)%s" % (col.fg('blue'), rec['channel'], col.attr(0))

        loctime = pytz.utc.localize(rec['time']).astimezone(tzlocal())
        print("%s%s%02d%s %s%s%s%s %s (%s)" % (
            col.fg('black'), col.bg(color), rec['level'], col.attr(0),

            col.fg('dark_green_sea'),
            loctime.strftime("%a, %d %b %Y %H:%M:%S"),
            col.attr(0),

            chan,
            rec['message'], host))

    for rec in reversed(list(db.find().sort('time', -1).limit(10))):
        _recprint(rec)
