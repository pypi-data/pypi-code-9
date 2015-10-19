# -*- coding: utf-8 -*-

from __future__ import absolute_import, print_function

import notify2
import os
from procfs import Proc as ProcFS

def notify(title, message="", icon="dialog-error", timeout=10000):
    if notify2 is not None:
        n = notify2.Notification(title, message, icon)
        n.timeout = timeout
        n.show()
    print(" => %s: %s" % (title, message))


def initialize_notify2():
    global notify2
    # Notify uses DBus to send notification to the user.
    # But MongoFS has to run as root.
    # Dang! We need some hacking to access the user's DBUS
    try:
        proc = ProcFS().self
        while True:         
            if proc.environ.get("DBUS_SESSION_BUS_ADDRESS") is not None:
                euid=os.geteuid()
                os.environ["DBUS_SESSION_BUS_ADDRESS"] = proc.environ["DBUS_SESSION_BUS_ADDRESS"]
                os.seteuid(int(proc.status["Uid"]["effective"]))
                try:
                    notify2.init("MongoFS")
                    break
                except:
                    pass
                finally:
                    os.seteuid(euid)
            proc = proc.parent
    except:
        notify2 = None
        notify("Cannot initialize notify2")


initialize_notify2()
