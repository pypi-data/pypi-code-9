#!/usr/bin/env python
from walt.server.postgres import PostgresDB
from time import time

EV_AUTO_COMMIT              = 0
EV_AUTO_COMMIT_PERIOD       = 2

class ServerDB(PostgresDB):

    def __init__(self):
        # parent constructor
        PostgresDB.__init__(self)
        # create the db schema
        self.execute("""CREATE TABLE IF NOT EXISTS devices (
                    mac TEXT PRIMARY KEY,
                    ip TEXT,
                    name TEXT,
                    reachable INTEGER,
                    type TEXT);""")
        self.execute("""CREATE TABLE IF NOT EXISTS topology (
                    mac TEXT REFERENCES devices(mac),
                    switch_mac TEXT REFERENCES devices(mac),
                    switch_port INTEGER);""")
        self.execute("""CREATE TABLE IF NOT EXISTS nodes (
                    mac TEXT REFERENCES devices(mac),
                    image TEXT);""")
        self.execute("""CREATE TABLE IF NOT EXISTS config (
                    item TEXT PRIMARY KEY,
                    value TEXT);""")
        self.execute("""CREATE TABLE IF NOT EXISTS logstreams (
                    id SERIAL PRIMARY KEY,
                    sender_mac TEXT REFERENCES devices(mac),
                    name TEXT);""")
        self.execute("""CREATE TABLE IF NOT EXISTS logs (
                    stream_id INTEGER REFERENCES logstreams(id),
                    timestamp TIMESTAMP,
                    line TEXT);""")

    # Some types of events are numerous and commiting the
    # database each time would be costly.
    # That's why we auto-commit every few seconds.
    def plan_auto_commit(self, ev_loop):
        ev_loop.plan_event(
            ts = time(),
            target = self,
            repeat_delay = EV_AUTO_COMMIT_PERIOD,
            ev_type = EV_AUTO_COMMIT
        )

    def handle_planned_event(self, ev_type):
        assert(ev_type == EV_AUTO_COMMIT)
        self.commit()

    def get_config(self, item, default = None):
        res = self.select_unique("config", item=item)
        if res == None:
            if default == None:
                raise RuntimeError(\
                    "Failed get_config(): item not found and no default provided.")
            self.insert("config", item=item, value=default)
            self.commit()
            return default
        else:
            return res.value

    def set_config(self, item, value):
        res = self.select_unique("config", item=item)
        if res == None:
            self.insert("config", item=item, value=value)
        else:
            self.update("config", "item", item=item, value=value)
