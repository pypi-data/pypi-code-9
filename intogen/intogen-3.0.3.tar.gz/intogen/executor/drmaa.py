import datetime
import difflib
import logging
import multiprocessing
import shlex
import sys
import os
import subprocess

import pkg_resources
from ruffus import cmdline
from ago import human

try:
    import pydevd
    DEBUGGING = True
except ImportError:
    DEBUGGING = False


try:
    import drmaa
    drmaa_enabled = True
except RuntimeError:
    drmaa_enabled = False

from intogen.executor.drmaa_wrapper import run_job, DrmaaError


class TaskExecutor(object):

    def __init__(self, options, scheduler_config, local_run=None, logger=None):

        self.options = options
        self.scheduler_config = scheduler_config
        self.local_run = local_run if local_run is not None else not drmaa_enabled
        self.times = {}

        self.jobs = scheduler_config.get('jobs')
        if self.options.jobs is not None:
            self.jobs = self.options.jobs

        self.default_queue = scheduler_config.get('queue')
        if len(self.options.queue) > 0:
            self.default_queue = self.options.queue

        if self.jobs is None:
            self.jobs = multiprocessing.cpu_count()

        # Initialize DRMAA session
        if drmaa_enabled:
            self.session = drmaa.Session()
            self.session.initialize()

    def run(self):

        start = datetime.datetime.now()
        cmdline.run(self.options, multithread=self.jobs)
        end = datetime.datetime.now()
        logging.info("Total execution time {0}".format(human(start - end)))

        if len(self.times) > 0:
            logging.info("Total computation time by task:")
            for t, v in self.times.items():
                msg = "        - '{0}' {1}".format(t, human(v['total']))
                if v['count'] > 1:
                    msg += " ({0} jobs took {1})".format(v['count'], human(v['total'] / v['count'], future_tense='in average {}'))
                logging.info(msg)
        else:
            logging.info("Everything up to date.")

    def submit(self, *args, scheduler=None, **kwargs):

        debug = self._get_scheduler_value(scheduler, "debug") is not None
        job_name = self._get_job_name(args, scheduler)

        # Log start
        start = datetime.datetime.now()
        logging.info("{0} [start]".format(job_name))

        # Run
        debug_job = (debug and DEBUGGING)
        if self.local_run or debug_job:
            self._submit_local(args, kwargs, scheduler, job_name, debugging=DEBUGGING)
        else:
            self._submit_remote(args, kwargs, scheduler, job_name)

        # Log end
        end = datetime.datetime.now()
        #pipeline_status_dict = get_pipeline_status()
        #incomplete_stats = incomplete_stats_string(pipeline_status_dict['incomplete'])
        #complete_stats =  complete_stats_string(pipeline_status_dict['complete'])
        #logging.info("{0} [done] ({1})\n\t\t\t\t{2}\n\t\t\t\t{3}".format(job_name, human(start - end), complete_stats, incomplete_stats))
        logging.info("{0} [done] ({1})".format(job_name, human(start - end)))

        self._accumulate_time(scheduler, start - end)

    def _submit_local(self, args, kwargs, scheduler, job_name, debugging=False):

        if not debugging:
            job_script_dir = self._get_job_dir(args)
            job_file_script = os.path.join(job_script_dir, job_name + ".sh")
            # job_file_stderr = os.path.join(job_script_dir, job_name + ".stderr")
            job_file_stdout = os.path.join(job_script_dir, job_name + ".log")
            job_file_stderr = job_file_stdout
            script, arguments = self._build_command(args, kwargs, scheduler)

            cmd = script + ' ' + arguments
            with open(job_file_script, "w") as script:
                script.write(cmd)

            ret_code = subprocess.call(cmd + " 2> " + job_file_stderr + " 1> " + job_file_stdout, shell=True)

            if ret_code != 0:
                with open(job_file_stderr) as stderr:
                    error = stderr.read()
                raise Exception("\n\nERROR WHILE RUNNING:\n   {0}\nOUTPUT:\n  {1}\n".format(cmd, error))

        else:
            # Otherwise we run the command in the main process to be
            # able to debug
            module = args[0]
            try:
                cmdline_method = getattr(module, 'cmdline')
            except AttributeError:
                raise RuntimeError("The module '" + module.__name__ + "' has no method run(...) defined.")

            script, arguments = self._build_command(args, kwargs, scheduler, search_installed_script=False)
            sys.argv = ["dummy-script"] + shlex.split(arguments)
            cmdline_method()

    def _build_command(self, args, kwargs, scheduler, search_installed_script=True):

        if search_installed_script:
            module = args[0]
            module_name = module.__name__
            distribution = module_name.split(".")[0]
            console_scripts = pkg_resources.get_entry_map(distribution, "console_scripts")
            script = None
            for entry_point in console_scripts.values():
                if entry_point.module_name == module_name:
                    script = entry_point.name
                    break
            if script is None:
                raise RuntimeError("There is no registered command line for the module: '" + module_name + "' Please re-install intogen")
        else:
            script = None

        inputs = args[1] if not isinstance(args[1], str) else [args[1]]
        outputs = args[2] if not isinstance(args[2], str) else [args[2]]
        arguments = []
        arguments = arguments + ['-i ' + i for i in inputs]
        arguments = arguments + ['-o ' + o for o in outputs]
        for k in kwargs:
            value = kwargs[k]
            if value is not None:
                if isinstance(value, bool):
                    if value:
                        arguments.append('--' + k)
                else:
                    option = str(value)
                    if " " in option:
                        option = "\"" + option + "\""
                    arguments.append('--' + k + ' ' + option)
        cores = self._get_scheduler_value(scheduler, 'cores')
        if cores is not None:
            arguments.append('--cores ' + str(cores))
        arguments = " ".join(arguments)
        return script, arguments

    def _submit_remote(self, args, kwargs, scheduler, job_name):

        script, cmd = self._build_command(args, kwargs, scheduler)
        cmd = script + ' ' + cmd

        # Remote execution
        try:

            if scheduler is None:
                scheduler = [script]

            stdout_res, stderr_res = "", ""

            job_script_dir = self._get_job_dir(args)

            stdout_res, stderr_res = run_job(
                cmd_str=cmd,
                job_name=job_name,
                drmaa_session=self.session,
                run_locally=self.local_run,
                job_other_options=self._get_job_other_options(scheduler),
                retain_job_scripts=True,
                job_script_directory=job_script_dir
            )

        # relay all the stdout, stderr, drmaa output to diagnose failures
        except DrmaaError as err:
            raise Exception("\n{0}\n{1}\n{2}\n{3}\n{4}\n".format(
                "Failed to run:",
                cmd,
                err,
                stdout_res,
                stderr_res))
        return cmd

    @staticmethod
    def _get_job_dir(args):

        outputs = args[2] if not isinstance(args[2], str) else [args[2]]

        if len(outputs) == 0:
            outputs = args[1] if not isinstance(args[1], str) else [args[1]]

        job_script_dir = os.path.join(os.path.dirname(outputs[0]), "logs")
        if not os.path.exists(job_script_dir):
            os.mkdir(job_script_dir)
        return job_script_dir

    @staticmethod
    def _get_job_name(args, scheduler):

        if scheduler is not None and len(scheduler) > 0:
            return scheduler[0]

        outputs = args[2] if not isinstance(args[2], str) else [args[2]]

        if len(outputs) == 0:
            return args[0].__name__

        if len(outputs) < 2:
            return os.path.basename(outputs[0])

        first = os.path.basename(outputs[0])
        last = os.path.basename(outputs[len(outputs)-1])
        matcher = difflib.SequenceMatcher(None, first, last)
        name = ""
        for block in matcher.get_matching_blocks():
            name += first[block[0]:(block[0]+block[2])]

        return name

    def _get_scheduler_value(self, scheduler, key, default=None):

        if self.scheduler_config is None or scheduler is None:
            return default

        for s in scheduler:
            task_config = self.scheduler_config.get(s, {})
            if key in task_config:
                return task_config[key]

        return default

    def _get_job_other_options(self, scheduler):

        queue = self._get_scheduler_value(scheduler, 'queue', self.default_queue)
        cores = self._get_scheduler_value(scheduler, 'cores', None)

        if queue is None:
            raise RuntimeError("You have to set the queue using -q parameter or at scheduler.conf file.")

        result = "-q '" + ",".join(queue) + "' -l 'qname=" + "|".join(queue) + "'"

        if cores is not None:
            result += " -pe serial " + str(cores)

        return result

    def _accumulate_time(self, scheduler, diff):

        if scheduler is None or len(scheduler) < 1:
            return

        key = scheduler[len(scheduler) - 1]
        if key in self.times:
            self.times[key]['total'] += diff
            self.times[key]['count'] += 1
        else:
            self.times[key] = { 'total': diff, 'count': 1 }