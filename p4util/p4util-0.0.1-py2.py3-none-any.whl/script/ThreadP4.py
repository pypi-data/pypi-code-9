#!/usr/bin/env python3

from __future__ import print_function

import threading
import P4
import sys
import argparse
import os, os.path
import re

NUMBER_OF_THREADS = 5

PATTERN = re.compile("Change (\d+) created.")

class SyncInThread(threading.Thread):
    def __init__(self, name, prepare, disable):
        threading.Thread.__init__(self)
        self.name = name
        self.prepare = prepare
        self.disable = disable
    
    def run(self):
        self.p4 = P4.P4()
        self.p4.connect()
        if self.disable:    
            self.p4.disable_tmp_cleanup()

        if self.prepare:
            self.create_files()
        else:
            self.sync_files()

        self.p4.disconnect()
        
    def create_files(self):
        os.mkdir(self.name)
        change = self.p4.fetch_change()
        change._description = "Created by {}".format(self.name)
        ch = self.p4.save_change(change)[0]
        
        m = PATTERN.match(ch)
        ch = m.group(1)
        
        for i in range(self.prepare):
            filename = os.path.join(self.name, "file{}".format(i))
            with open(filename, "w") as f:
                f.write("Some stuff\n" * 100)
            self.p4.run_add("-c", ch, filename)
        result = self.p4.run_submit("-c", ch)
        print("{} submitted {}".format(self.name, ch))
        
    def sync_files(self):
        total = self.p4.run_sync("-f", "{}/...".format(self.name))
        print("{} synced {} files".format(self.getName(), len(total)))
    
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    
    parser.add_argument('-p', '--prepare', type=int, help = "Prepare the sync by creating dirs and files first")
    parser.add_argument('-d', '--disable', action='store_true', help = "Enable thread safety by disabling the cleanup of tmps")
    parser.add_argument('-n', '--name', default="test", help = "Directory Prefix (default = test)")
    parser.add_argument('-t', '--threads', type=int, default=NUMBER_OF_THREADS, help="Number of threads (default = 5)")
    
    options = parser.parse_args()
    
    for i in range(options.threads):
        t = SyncInThread(options.name + str(i), options.prepare, options.disable)
        t.start()
