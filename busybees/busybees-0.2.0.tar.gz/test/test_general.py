import threading
import time
import sys

from busybees import worker
from busybees import hive

import pash

class ErrWorker(worker.Worker):
    def work(self, command):
        proc = pash.ShellProc()
        proc.run(command)
        return "Exit code: %s" % proc.get_val('exit_code')

def test_hive():
    apiary = hive.Hive()
    apiary.create_queen('A1')
    apiary.create_queen('A2')
    apiary.start_queen('A1')
    apiary.start_queen('A2')

    job1 = ["iscsiadm -m discovery -t st -p 192.168.88.110",
            "iscsiadm -m discovery -t st -p 192.168.90.110",
            "iscsiadm -m discovery -t st -p 192.168.88.110"]
    apiary.instruct_queen('A1', job1, ErrWorker)

    job2 = ["ls -l ~", "date", "cal"]
    apiary.instruct_queen('A2', job2)

    apiary.kill_queen('A1')

    time.sleep(3)

    results = apiary.die()

    for key in results.keys():
        for i in results[key]:
            assert i != '' and i != None
