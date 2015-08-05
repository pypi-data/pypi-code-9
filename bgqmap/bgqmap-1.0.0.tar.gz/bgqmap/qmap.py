import argparse
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor
import datetime
import logging
import os
from ago import human
import sys
from bgqmap.drmaa_wrapper import DrmaaError, run_job
from bgqmap.utils import NonBlockingConsole, count_lines
from time import sleep

try:
    import drmaa
    RUN_LOCAL = False
except Exception:
    RUN_LOCAL = True


class QMapExecutor(object):

    def __init__(self, queue, max_jobs, cores, output_folder=None, commands_per_job=1, force_local=False, max_jobs_file=None, interactive=True, adaptative=True):

        # Decide if we have to run locally or not
        self.run_local = RUN_LOCAL if not force_local else True
        self.interactive = interactive
        self.adaptative = adaptative

        # Define queue to use
        self.queue = queue if len(queue) != 0 else ['normal']

        # Cores
        self.cores = cores

        # Read max jobs file
        self.max_jobs_file = max_jobs_file if max_jobs_file is not None and os.path.exists(max_jobs_file) else None
        if self.max_jobs_file is not None:
            if not os.path.isabs(self.max_jobs_file):
                self.max_jobs_file = os.path.join(os.getcwd(), self.max_jobs_file)

        # Update max_jobs
        self.max_jobs = max_jobs
        self._update_max_jobs()

        # Initialize DRMAA session
        if not self.run_local:
            self.session = drmaa.Session()
            self.session.initialize()
            self.pool = ThreadPoolExecutor
        else:
            self.session = None
            self.pool = ProcessPoolExecutor
            if not force_local and self.max_jobs > os.cpu_count():
                self.max_jobs = os.cpu_count()

        # Set default output folder
        self.output_folder = output_folder
        if self.output_folder is None:
            self.output_folder = os.path.join(os.getcwd(), 'output')

        if not os.path.exists(self.output_folder):
            os.mkdir(self.output_folder)

        # Number of commands to put in a single job
        self.commands_per_job = commands_per_job

    def exit(self):
        if self.session is not None:
            self.session.exit()

    def _update_max_jobs(self):
        if self.max_jobs_file is None:
            if self.max_jobs == 0:
                if self.cores == 0:
                    self.max_jobs = os.cpu_count()
                else:
                    self.max_jobs = self.cores
        else:
            try:
                with open(self.max_jobs_file, 'r') as f:
                    num = int(f.readline())
                    if self.max_jobs != num:
                        self.max_jobs = num
                        logging.info("Setting max running jobs to %d", self.max_jobs)

            except ValueError:
                logging.error("Reading max jobs file")
                self.max_jobs = os.cpu_count()

    def _send_jobs(self, executor, future_to_jobs, command, arguments_enumerate, jobs_to_submit, job_name, done_args):

        jobs_skip = 0
        jobs = []
        arguments_bag = []
        name = None
        jobs_count = 0
        while jobs_count < jobs_to_submit:

            try:
                cmd_count, cmd_args = next(arguments_enumerate)
            except StopIteration:
                break

            if name is None:
                name = "{0}-{1}".format(job_name, cmd_count)

            if cmd_args not in done_args:
                arguments_bag.append(cmd_args)
                if len(arguments_bag) == self.commands_per_job:
                    jobs.append({'name': name, 'command': command, 'arguments': arguments_bag})
                    jobs_count += 1
                    arguments_bag = []
                    name = None
            else:
                jobs_skip += 1

        for job in jobs:
            future = executor.submit(
                self.start_job,
                job['command'],
                job['arguments'],
                job['name'],
                self.output_folder
            )
            future_to_jobs[future] = job

        return future_to_jobs, jobs_skip

    @staticmethod
    def _choose_option(valid_options):
        while True:
            try:
                print('Choose one option: ')
                option = int(sys.stdin.read(1))
                if option in valid_options:
                    break
            except ValueError:
                pass

            print("[not a valid option]")

        return option

    def _wait_jobs(self, executor, future_to_jobs, abort_submiting):
        done = []

        with NonBlockingConsole(interactive=self.interactive) as nbc:

            sleep_count = 0
            while len(done) == 0:

                done = set([future for future in future_to_jobs.keys() if future.done()])

                sleep(0.1)
                sleep_count += 1
                if sleep_count > 50 or len(done) > 0:
                    sleep_count = 0
                    if self.max_jobs_file is not None:
                        self._update_max_jobs()

                if nbc.get_data() == '\x1b':  # x1b is ESC

                    print("----------------------------------")
                    print(" 1. Wait pending jobs and exit    ")
                    print(" 2. Exit immediately              ")
                    print(" 3. Continue submiting jobs       ")
                    print(" 4. Change maximum running jobs   ")
                    if not self.run_local:
                        print(" 5. Change queues                 ")
                    print("----------------------------------")

                    valid_options = [1, 2, 3, 4]
                    if not self.run_local:
                        valid_options.append(5)
                    option = self._choose_option(valid_options)

                    if option == 1:
                        print("[waiting pending jobs and aborting]")
                        abort_submiting = True
                        continue
                    elif option == 2:
                        print("[exit immediately]")
                        done = set()
                        future_to_jobs = {}
                        abort_submiting = True
                        break
                    elif option == 3:
                        print("[continue submiting jobs]")
                        continue
                    elif option == 4:
                        print("[change maximum running jobs]")
                        nbc.__exit__(None, None, None)
                        try:
                            self.max_jobs = int(input("From {} jobs to: ".format(self.max_jobs)))
                            executor._max_workers = self.max_jobs
                            if self.run_local:
                                executor._adjust_process_count()
                            else:
                                executor._adjust_thread_count()
                            print("[jobs changed to {}]".format(self.max_jobs))
                            done = set()
                            break
                        except ValueError:
                            print("[invalid integer, continue submiting jobs]")
                            continue
                        finally:
                            nbc.__enter__()
                    elif option == 5:
                        print("[change queues (use comma to separate multiple queuues)]")
                        nbc.__exit__(None, None, None)
                        try:
                            queues = str(input("From '{}' queues to: ".format(','.join(self.queue)))).split(',')
                            if len(queues) > 0:
                                self.queue = [q.strip() for q in queues]
                            else:
                                print("[invalid input, continue submiting jobs]")
                                continue
                            print("[queues changed to '{}']".format(','.join(self.queue)))
                        except ValueError:
                            print("[invalid input, continue submiting jobs]")
                            continue
                        finally:
                            nbc.__enter__()

        return abort_submiting, done, future_to_jobs

    def run(self, command, arguments, arguments_size, job_name=None):
        """

        :param command: Command to run
        :param arguments: Iterator to arguments to run in parallel
        :param arguments_size: Total size of arguments
        :param job_name: Job name (by default will use command file name)
        :return: jobs_done, jobs_fail, jobs_skip
        """

        # Set a default job name
        if job_name is None:
            job_name = os.path.basename(command)

        # Check if the command is in the current folder
        if not os.path.isabs(command):
            command_abs = os.path.abspath(command)
            if os.path.exists(command_abs):
                # Otherwise it must be in the PATH or it will fail
                command = command_abs

        # Files with done and fail arguments
        err_args_file = os.path.join(self.output_folder, job_name + ".map.err")
        done_args_file = os.path.join(self.output_folder, job_name + ".map.done")

        if os.path.exists(done_args_file):
            with open(done_args_file, 'r') as done_fd:
                done_args = set(done_fd.readlines())
        else:
            done_args = set()

        commands_skip = 0
        arguments = enumerate(arguments, start=1)
        with self.pool(max_workers=self.max_jobs) as executor, \
                open(err_args_file, 'a') as err_args_fd, \
                open(done_args_file, 'a') as done_args_fd:

            # Start sending jobs
            jobs_done = 0
            jobs_fail = 0
            abort_submiting = False
            last_increased = 0
            jobs_total = int(arguments_size / self.commands_per_job)

            start = datetime.datetime.now()
            elapsed_total = datetime.timedelta()

            future_to_jobs, skip = self._send_jobs(executor, {}, command, arguments, self.max_jobs, job_name, done_args)
            commands_skip += skip

            while len(future_to_jobs) > 0:

                jobs_skip = int(commands_skip / self.commands_per_job)

                abort_submiting, done, future_to_jobs = self._wait_jobs(executor, future_to_jobs, abort_submiting)
                not_done = set(future_to_jobs.keys()) - done

                # Process done jobs
                for future in done:

                    if not future in future_to_jobs:
                        continue

                    job = future_to_jobs.pop(future)

                    try:

                        try:
                            elapsed = future.result()
                        except KeyboardInterrupt:
                            logging.warning("Job {} was keyboard interupted".format(job['name']))
                            continue

                        elapsed_total += elapsed
                        jobs_done += 1
                        elapsed_average = elapsed_total / jobs_done

                        # TODO improve remaining time prediction
                        # jobs_pending = jobs_total - jobs_skip - jobs_done - jobs_fail - len(not_done)
                        # remaing = elapsed_average * (jobs_pending / self.max_jobs)
                        # now = datetime.datetime.now()

                        logging.info(
                            "%s [end] (%s - %d/%d) ",
                            job['name'], human(elapsed), jobs_done + jobs_fail + jobs_skip, jobs_total
                        )

                        for arg in job['arguments']:
                            done_args_fd.write(arg)

                        if not self.run_local and self.adaptative:
                            # At a cluster with a queue system we want jobs of at least 5 minutes long
                            # NOTE: all timedelta are negative values
                            five_minutes = datetime.timedelta(minutes=-5)
                            if elapsed_average > five_minutes and (jobs_done - last_increased) > self.max_jobs:
                                inc = int(self.commands_per_job * (five_minutes / elapsed_average)) - self.commands_per_job
                                if inc > 0:
                                    last_increased = jobs_done
                                    self.commands_per_job += inc
                                    jobs_total = int(arguments_size / self.commands_per_job)
                                    logging.warning("Increasing the number of commands per job to %d", self.commands_per_job)

                    except RuntimeError:
                        jobs_fail += 1
                        logging.error('{} [fail]'.format(job['name']))
                        for arg in job['arguments']:
                            err_args_fd.write(arg)

                # Submit new jobs
                jobs_to_submit = self.max_jobs - len(not_done)
                if not abort_submiting and jobs_to_submit > 0:
                    future_to_jobs, skip = self._send_jobs(executor, future_to_jobs, command,
                                                           arguments, jobs_to_submit, job_name, done_args)
                    commands_skip += skip

            end = datetime.datetime.now()
            logging.info("jobs = (%d done, %d fail, %d skip) time = (%s)", jobs_done, jobs_fail, commands_skip, human(start - end))

            return jobs_done, jobs_fail, commands_skip

    def start_job(self, command, arguments, job_name, job_script_dir):

        if isinstance(self.queue, dict):
            queue = self.queue[arguments[0]]
        else:
            queue = self.queue

        if isinstance(self.cores, dict):
            cores = max([self.cores[a] for a in arguments])
        else:
            cores = self.cores

        stdout_res, stderr_res = "", ""
        try:

            job_options = "-q '" + ",".join(queue) + "' -l 'qname=" + "|".join(queue) + "'"

            if cores > 1:
                job_options += " -pe serial " + str(cores)

            start = datetime.datetime.now()
            logging.info("%s [start]", job_name)
            stdout_res, stderr_res = run_job(
                cmd_str='\nerr=$?; if [ $err -ne 0 ]; then exit $err; fi\n'.join([' '.join([command, a]) for a in arguments]),
                job_name=job_name,
                drmaa_session=self.session,
                run_locally=self.run_local,
                job_other_options=job_options,
                retain_job_scripts=True,
                job_script_directory=job_script_dir
            )
            return start - datetime.datetime.now()

        # relay all the stdout, stderr, drmaa output to diagnose failures
        except DrmaaError:
            raise RuntimeError("{0}\n{1}\n{2}\n".format(
                command,
                stdout_res,
                stderr_res))


def cmdline():
    # Config logging
    logging.basicConfig(format='%(asctime)s %(levelname)s: %(message)s', datefmt='%H:%M:%S', level=logging.INFO)

    # Parse arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--command', dest='command', required=True,
                        help='The script that you want to execute')
    parser.add_argument('-m', '--map_file', dest='map_file', default=None, required=True,
                        help='The file with the command arguments that you want to map')
    parser.add_argument('-j', '--max_jobs', dest='max_jobs', default=0, type=int,
                        help='Maximum running jobs')
    parser.add_argument('--max_jobs_file', dest='max_jobs_file', default=None,
                        help='A file with the number of maximum jobs to run (it can change while runnning)')
    parser.add_argument('-o', '--output_folder', dest='output_folder', default=None,
                        help="Output folder (by default it will create an 'output' folder in the current folder)")
    parser.add_argument('-n', '--job_name', dest='job_name', default=None,
                        help="A prefix for your jobs")
    parser.add_argument('-q', '--queue', dest='queue', action='append', default=[],
                        help='Cluster queues')
    parser.add_argument('--cores', dest='cores', default=0, type=int,
                        help='In a cluster, the number of cores that will use each process')
    parser.add_argument('--force_local', dest='force_local', default=False, action="store_true",
                        help='If you are in a cluster environment this will force the qmap to run only in '
                             'current machine')
    parser.add_argument('--commands_per_job', dest='commands_per_job', default=1, type=int,
                        help="If the execution of one command is very fast, then it's better to increase the commands"
                             " per jobs to run several commands at the same core, without rescheduling it again.")
    parser.add_argument('--adaptative', dest='adaptative', default=False, action="store_true",
                        help='Dynamically change commands_per_job to have tasks of at least 5 minutes')

    options = parser.parse_args()

    # Open and load arguments map file.
    map_file = options.map_file
    if not os.path.isabs(map_file):
        map_file = os.path.abspath(map_file)

    arguments_size = count_lines(map_file)

    with open(map_file, 'r') as arguments:

        # Execute all processes concurrently

        executor = QMapExecutor(
            options.queue,
            options.max_jobs, options.cores,
            force_local=options.force_local,
            output_folder=options.output_folder,
            commands_per_job=options.commands_per_job,
            max_jobs_file=options.max_jobs_file,
            adaptative=options.adaptative
        )

        executor.run(
            options.command,
            arguments,
            arguments_size,
            job_name=options.job_name
        )


if __name__ == "__main__":
    cmdline()




