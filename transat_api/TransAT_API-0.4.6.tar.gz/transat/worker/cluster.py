from worker import Worker
from transat.communicator.communicator import Communicator
import os
import time

runfile_pbs = """\
#!/bin/sh
## job name
#$ -N "{name}"
## interpreting shell for the job
#$ -S /bin/sh

## to execute job from current working directory
#$ -cwd

## to merge standard error output with standard output
#$ -j y

## to submit current environment variables to job
#$ -V
## defines the parallel environment
##    orte for openMPI
## and the number of nodes, e.g. 64
#$ -pe orte {nprocs}
touch simulation.started
rm simulation.finished
{cmd}
rm transatmbinitialDP
rm simulation.started
touch simulation.finished
"""


class Cluster(Worker):
    def __init__(self, host, username):
        """Summary line.

        Extended description of function.

        Args:
            arg1 (int): Description of arg1
            arg2 (str): Description of arg2

        Returns:
            bool: Description of return value

        """
        super(Cluster, self).__init__(host)
        self.com = Communicator(host, username)

    def execute(self, task, nproc=0, queue=None):
        self.com.run_cmd(task.cmd)
        print "Executing command: " + task.cmd

    def get_pbs_string(self, name, nprocs, cmd):
        return runfile_pbs.format(**{'name': name, 'nprocs': nprocs, 'cmd': cmd})

    def ssh(self, cmd, args):
        return self.com.run_cmd(cmd, args['wd'])

    def qsub(self, cmd, args):
        filename = 'run.pbs'
        self._create_submission_file(args['wd'], cmd, args['name'], args['nprocs'], filename)
        job_id = self._submit_job(args['wd'], filename)
        print "submission file submited with id "+str(job_id)
        try:
            self._watch_job(job_id, args['wd'])
        except KeyboardInterrupt:
            self._del_job(job_id, args['wd'])
            raise
        success = self._check_status(job_id, args['name'], args['wd'])
        return success

    def _submit_job(self, wd, filename):
        cmd = 'source /etc/profile ; qsub ' + filename
        code, output, error = self.com.run_cmd(cmd=cmd, wd=wd)
        if code == 0:
            job_id = output.read().split(" ")[2]
            print "job " + str(job_id) + " submitted"
            return job_id
        else:
            print output.readlines()
            print error.readlines()
            print "error in submit job"
            raise

    def _watch_job(self, job_id, wd):
        running = False
        started = False
        while started is False:
            time.sleep(2)
            code, output, error = self.com.run_cmd(cmd='ls -s simulation.started', wd=wd)
            if len(output.readlines()) > 0:
                started = True
                running = True

        while running:
            time.sleep(2)
            code, output, error = self.com.run_cmd(cmd='ls -s simulation.finished', wd=wd)
            if len(output.readlines()) > 0:
                running = False

    def _check_status(self, job_id, name, wd):
        code, output, error = self.com.run_cmd(cmd='ls -s ' + str(name) + '.po' + str(job_id), wd=wd)
        return output.readlines()[0].split()[0] == '0'

    def _create_submission_file(self, wd, cmd, name, nprocs, filename):
        pbs_string = self.get_pbs_string(name, nprocs, cmd)
        self.com.run_cmd(cmd='echo "' + pbs_string + '">' + filename, wd=wd)

    def _del_job(self, job_id, wd):
        cmd = 'source /etc/profile ; qdel ' + str(job_id)
        print "qdel job id : " + str(job_id)
        code, output, error = self.com.run_cmd(cmd=cmd, wd=wd)
