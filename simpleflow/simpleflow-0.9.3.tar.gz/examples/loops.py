import random as _random
import time

from simpleflow import (
    activity,
    Workflow,
    futures,
)


def as_activity(func):
    """
    This decorator provides default values for the activities's attributes.
    We should rather decorate each activity individually to set the right
    values, especially for timeouts.
    """
    return activity.with_attributes(
        version='1.0',
        task_list='example',
        schedule_to_start_timeout=54000,  # 15h
        start_to_close_timeout=21600,     # 6h
        schedule_to_close_timeout=75600,  # 21h
        heartbeat_timeout=10000,  # High right now to be tested in standalone mode
        retry=1,
        raises_on_failure=True,
    )(func)

def random(*args):
    print "args: {}".format(args)
    time.sleep(_random.random())
    return True

merge_files_from_date = as_activity(random)
make_statuses_file = as_activity(random)


class UpdateWorkflow(Workflow):
    name = 'update'
    version = 'example'
    task_list = 'example'

    def submit(self, func, *args, **kwargs):
        future = super(UpdateWorkflow, self).submit(func, *args, **kwargs)
        print "submitted future {}(args={}, kwargs={})".format(func, args, kwargs)
        return future

    def run(self, nb_blocks):
        wait_for_bq_tables = []

        for block in xrange(0, nb_blocks):
            daily_merge_activities = self.compute_daily_merge(block)
            wait_for_bq_tables += daily_merge_activities

            if all(i.finished for i in daily_merge_activities):
                statuses_activities = self.compute_statuses(block)
                wait_for_bq_tables += statuses_activities

        futures.wait(*wait_for_bq_tables)
        return "foo"

    def compute_daily_merge(self, block):
        merge_activities = []
        all_dates = ["20150919", "20150920", "20150921"]
        for current_date in all_dates:
            a = self.submit(
                merge_files_from_date,
                all_dates,
                block)
            merge_activities.append(a)
        return merge_activities

    def compute_statuses(self, block):
        activities = []
        all_dates = ["20150919", "20150920", "20150921"]
        for se_id in [1, 2]:
            activity = self.submit(
                make_statuses_file,
                block,
                se_id)
            activities.append(activity)
        return activities
