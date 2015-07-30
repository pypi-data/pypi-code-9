import datetime, sys, traceback
from datetime import datetime, timedelta

from malibu.design import borgish
from malibu.util.decorators import function_registrator


class Scheduler(borgish.SharedState):

    def __init__(self):

        super(Scheduler, self).__init__()

        self.__jobs = {}

    def create_job(self, name, func, delta, recurring = False):
        """ Creates a new job instance and attaches it to the scheduler.
            
            Params
            ------
            name : str
                Name of the job to create.
            func : function
                Function that is specified as the execution callback.
            delta : datetime.timedelta
                Timedelta to execute on.
            recurring : bool, optional
                Whether the job should continue running after first run.

            Raises
            ------
            SchedulerException
                If the job already exists, func is none, or delta is not
                an instance of datetime.timedelta.

            Returns
            -------
            SchedulerJob
                If job creation was succesful.
        """

        if name in self.__jobs:
            raise SchedulerException("Job already exists; remove it first.")
        if func is None:
            raise SchedulerException("Callback function is non-existent.")
        if not isinstance(delta, timedelta):
            raise SchedulerException("Argument 'delta' was not a timedelta instance.")

        job = SchedulerJob(name, func, delta, recurring)
        self.add_job(job)

        return job

    def add_job(self, job):
        """ Adds a job to the list of jobs maintained by the scheduler.

            Params
            ------
            job : SchedulerJob
                Job to add to the list of active jobs.

            Raises
            ------
            SchedulerException
                If the job already exists in the jobs dictionary.
        """

        if job in self.__jobs:
            raise SchedulerException("Job already exists; remove it first.")

        job.begin_ticking()
        self.__jobs.update({job.get_name() : job})

    def remove_job(self, name):
        """ Removes a job from the list of jobs maintained by the scheduler.
        
            Params
            ------
            name : str
                Name of the job to remove from the job list.

            Raises
            ------
            SchedulerException
                If the job does not exist.
        """

        if name not in self.__jobs:
            raise SchedulerException("Job does not exist.")

        self.__jobs.pop(name)

    def tick(self):
        """ Gets the current time and checks the ETA on each job.
            If the job is ready, it executes and captures any exception
            that should raise out of the execute call.
            If an exception is capture, the job's onfail callbacks will be
            fired with a reference to the job object that was being triggered.
        """

        now = datetime.now()

        for job in self.__jobs.values():
            if job.is_ready(now):
                try:
                    job.execute()
                    job.set_traceback(None)
                except Exception as e:
                    job.set_traceback(e)
                    job.fire_onfail()
                if not job.is_recurring():
                    self.remove_job(job.get_name())
                else:
                    self.remove_job(job.get_name())
                    self.add_job(job)


class SchedulerJob(object):

    def __init__(self, name, function, delta, state, recurring = False):

        self._scheduler = Scheduler()
        self._name = name
        self._function = function
        self._delta = delta
        self._recurring = recurring
        self._last_traceback = None
        self._onfail = []
        self.onfail = function_registrator(self._onfail)

        self._eta = delta

    def get_name(self):

        return self._name

    def get_eta(self):

        return self._eta

    def get_traceback(self):

        return self._last_traceback

    def set_traceback(self, stack):

        self._last_traceback = stack

    def attach_onfail(self, func):

        self._onfail.append(func)

    def detach_onfail(self, func):

        self._onfail.remove(func)

    def fire_onfail(self):

        for callback in self._onfail:
            callback(job = self)

    def is_recurring(self):

        return self._recurring

    def is_ready(self, time):

        if time >= self._eta:
            return True
        else:
            return False

    def begin_ticking(self):

        self._eta = datetime.now() + self._delta

    def execute(self):

        self._function()

        if self._recurring:
            self._eta += self._delta


class SchedulerException(Exception):

    def __init__(self, value):

        self.value = value

    def __str__(self):

        return repr(self.value)
