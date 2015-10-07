"""
Provides a helper class for the mutation and scoring binaries,
to run and distribute work to multiple instances of them.
"""

# TODO: there's lots of bugs in this code.

import json
import os
import select
import signal
import subprocess

def on_sig_child(signum, frame):
    # This is not a bug in *this* program, it happens when a process managed by
    # this code dies.
    # Don't rely on this happening! There are subtle bugs in the code below.
    raise RuntimeError('Child task died.')

def install_signal_handler():
    signal.signal(signal.SIGCHLD, on_sig_child)

def is_signal_handler_installed():
    return signal.getsignal(signal.SIGCHLD) == on_sig_child

class TaskState:
    PENDING = 0
    INPUT = 1
    PROCESSING = 2
    OUTPUT = 3

class Task(object):
    def __init__(self, args, shell=False):
        self.args = args

        env = dict(os.environ)
        env['PYTHONUNBUFFERED'] = '1'

        self.process = subprocess.Popen(
            args=self.args,
            shell=shell,
            env=env,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            bufsize=1, # line-buffered.
        )
        self.state = TaskState.PENDING
        self.task_id = None

    def start_select(self, rlist, wlist):
        if self.state == TaskState.PENDING:
            wlist.append(self.process.stdin)
        if self.state == TaskState.PROCESSING:
            rlist.append(self.process.stdout)

    def finish_select(self, rlist, wlist):
        if (
            self.state == TaskState.PENDING and
            self.process.stdin in wlist
        ):
            self.state = TaskState.INPUT
        if (
            self.state == TaskState.PROCESSING and
            self.process.stdout in rlist
        ):
            self.state = TaskState.OUTPUT

    def write(self, obj, task_id):
        assert self.state == TaskState.INPUT
        assert self.task_id is None
        self.task_id = task_id

        data = json.dumps(obj)
        self.process.stdin.write(data + '\n')
        self.process.stdin.flush()
        self.state = TaskState.PROCESSING

    def read(self):
        assert self.state == TaskState.OUTPUT
        assert self.task_id is not None

        data = self.process.stdout.readline()
        self.state = TaskState.PENDING

        task_id = self.task_id
        self.task_id = None

        return task_id, json.loads(data.rstrip('\n'))

    def __repr__(self):
        return '<Task %r state=%r task_id=%r>' % (
            self.args,
            self.state,
            self.task_id,
        )

class Job(object):
    def __init__(self, args, num_tasks, shell=False):
        self.tasks = [
            Task(args, shell=shell)
            for _ in range(num_tasks)
        ]

    def update_task_states(self):
        rlist = []
        wlist = []
        for task in self.tasks:
            task.start_select(rlist, wlist)
        if not (rlist or wlist):
            return
        rlist, wlist, _ = select.select(rlist, wlist, [])
        for task in self.tasks:
            task.finish_select(rlist, wlist)

    def _map(self, inputs):
        assert is_signal_handler_installed()
        inputs = iter(inputs)
        consumed_input = False
        n_input = 0
        n_output = 0
        while not consumed_input or (n_input > n_output):
            # Find out which tasks are ready for input.
            self.update_task_states()

            # Read output, give input.
            for task in self.tasks:
                if task.state == TaskState.OUTPUT:
                    value = task.read()
                    yield value
                    n_output += 1
                if not consumed_input and task.state == TaskState.INPUT:
                    try:
                        value = next(inputs)
                        task.write(value, n_input)
                        n_input += 1
                    except StopIteration:
                        consumed_input = True

    def map_unordered(self, inputs):
        return (result for _, result in self._map(inputs))

    def map(self, inputs):
        results = self._map(inputs)
        return [result for _, result in sorted(results)]
