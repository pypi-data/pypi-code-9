import time

from simpleflow import activity, Workflow, futures


@activity.with_attributes(task_list="test", version="1.0")
def first_activity(block):
    print "start first_activity for block {}".format(block)
    if block == 0:
        time.sleep(5)
    else:
        time.sleep(1)
    print "finish first_activity for block {}".format(block)


@activity.with_attributes(task_list="test", version="1.0", idempotent=True)
def second_activity(block):
    print "triggered second_activity for block {}".format(block)


class ChangingWorkflow(Workflow):
    name = "changing"
    version = "1.0"
    task_list = "test"

    def run(self):
        _all = []

        for block in [0, 1]:
            first = self.submit(first_activity, block)
            _all.append(first)

            if first.finished:
                second = self.submit(second_activity, block)
                _all.append(second)

        futures.wait(*_all)
