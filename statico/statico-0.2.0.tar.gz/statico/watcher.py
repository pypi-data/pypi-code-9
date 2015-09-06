# -*- coding: utf-8 -*-
"""
    statico.watcher
    ---------------
    Defines a file watcher using linux's inotify
    :license: MIT, see LICENSE for more details.
"""
import pyinotify
from .tasks import generate_task

# Set up pyinotify export methods to start a blocking loop
# watcher = Watcher(handler());
# watcher.register('/tmp');
# watcher.start(); # This will block
class Watcher(object):
    def __init__(self, handler=None):
        if handler is None:
            handler = WatcherEvent()
            
        self.__wm = pyinotify.WatchManager()
        self.__notifier = pyinotify.Notifier(self.__wm, handler)

    def register(self, path):
        self.__wm.add_watch(path, (pyinotify.IN_DELETE | pyinotify.IN_CREATE | pyinotify.IN_MODIFY), rec=True)
    
    def start(self):
        self.__notifier.loop()

# Callback handler
# __call__ is runs when any method is called (keeps the code small) and is passed
# event, which holds details about the changed file.
class WatcherEvent(pyinotify.ProcessEvent):
    def __call__(self, event):
        print('> ' + event.maskname + ': ' + event.name)
        generate_task(verbose=False)
