__author__ = 'anna'

import paramiko
import cmd
import re
import sys
import os
import ConfigParser
QSUB_CONFIG = ['-N','-pe','-t','-q']
class HPCJobManager():
    error_log = ""
    def connect(self, configfile):
        """ Connect to the host
            Keyword arguments:
            configfile - path to configuration file, string.
            It must contain:
            host -- host name to connect to , string
            username -- username on the remote server, string
            password -- password for username on the remote server, string
        """
        try:
            self.ssh = paramiko.SSHClient()
            self.ssh.set_missing_host_key_policy(
            paramiko.AutoAddPolicy())
            self.config = ConfigParser.ConfigParser()
            self.config.read(configfile)
            host = self.config.get('connection', 'HOST')
            username = self.config.get('connection', 'USERNAME')
            password = self.config.get('connection', 'PASSWORD')
            self.ssh.connect(host.strip(), username=username.strip(),
            password=password.strip())

        except:
            self.error_log += "\n could not connect to host " +str(sys.exc_info()[0])

    def disconnect(self):
        self.ssh.close()

    def run_cmd(self,command):
        """ run command
            Keyword arguments:
            command -- command to execute, string
            Returns:
            outputString, string
        """
        outputString = ''
        try:
            stdin, stdout, stderr =self.ssh.exec_command(command)
            outputString = str(stdout.read())
        except:
            self.error_log += "\n exception in run command " +str(sys.exc_info()[0])
        return outputString
    #error examples:
   #qsub: ERROR! invalid option argument "-www"
    def submit_cmd (self, job_command,configpath=None, cwd = None, name = None,options = None ):
        """ submit job
            Keyword arguments:
            configpath - path to config file
            options - dict
            job_command -- job to execute, string
            cwd  - directory path, string
            name - name for output file, string
            Returns:
            jobid = JOB_ID for submitted job, str
            Possible Options for job submission:
            -N filename
            -q long/short
            -t repeat
            -pe parallel_environment

        """
        jobid = '0'

        try:
            command = self.create_submit_command(configpath,cwd, name, options,"qsub.orig")
            # filename = self.create_submit_script(job_command, name, options)
            # jobid = self.run_job_cmd(command,filename) #filename is the name of the script
            stdin, stdout, stderr = self.ssh.exec_command(command)
            nextline = "#!/bin/bash\n" + job_command + "\n"
            stdin.channel.sendall(nextline)
            stdin.channel.shutdown_write()
            outputString = stdout.read()
            try:
                jobid = outputString.split()[2]
            except:
                try:
                     if 'ERROR' in outputString:
                         self.error_log +=  "\nerror in interactive job command execution " + outputString
                     else:
                          self.error_log += "\n lack of response " +str(sys.exc_info()[0])
                except:
                    self.error_log += "\n error in job submission response " +str(sys.exc_info()[0])

        except:
            self.error_log += "\n exception in job submission " +str(sys.exc_info()[0])
        return jobid
   #error examples:
   #qsub: ERROR! invalid option argument "-www"
    def submit(self,script_name,configpath=None, cwd = None, name = None,options = None ):
        """ submit job
            Keyword arguments:
            configpath - path to config file
            options - dict
            script_name -- script to execute, string
            cwd  - directory path, string
            name - name for output file, string
            Returns:
            jobid = JOB_ID for submitted job, str
            Possible Options for job submission:
            -N filename
            -q long/short
            -t repeat
            -pe parallel_environment

        """
        jobid = '0'
        try:
            command = self.create_submit_command(configpath,cwd, name, options, "qsub")
            #print '\n created command ', command
            jobid = self.run_job_cmd(command, script_name)
        except:
            self.error_log += "\n exception in job submission " +str(sys.exc_info()[0])
        return jobid

    def create_submit_command(self,configpath, cwd, name,options,qsub_command):
        """ create job submission command
         Keyword arguments:
         configpath - path to config file
         options - dict
         cwd  - directory path, string
         name - name for output file, string
         qsub_command - qsub wrappter command (or qsub.orig), string
         Returns:
         command - string

        """

        #self.config.read('config/qsub.config')
        if configpath is None:
            allowed_options = QSUB_CONFIG
        else:
            self.config.read(configpath)
            allowed_options = self.config.get('options', 'CMD_OPTIONS')

        if options is None:
            options = {}

        command = ""
        for k in options.keys():
            if k in allowed_options:
                command +=  " " + str(k) + " " + options[k] + " "
            else:
                self.error_log += "\n invalid option for qsub "

        if name is not None:
            if options.__contains__('-N'):
                pass
            else:
                command +=  " " + "-N" + " " + str(name) + " "

        if cwd is not None:
            command = "cd " + str(cwd) +  " ; " + qsub_command + " " + command #+ " " + job_command
        else:
            command =  qsub_command + " " + command #+ " " + job_command
        #print '\n command after all is ', command

        return command

    def create_submit_script(self,job_command, name,options):
        sftp = self.ssh.open_sftp()
        filename = "myscript.sh"

        if os.path.isfile("test/"+filename): #todo:double check
            os.remove()
        else:
            try:
                sftp.mkdir('test')
            except IOError:
                pass
        f = sftp.open('test' + '/' + filename, 'w')
        f.write("#!/bin/bash")
        f.write('\n')
        f.write(job_command)
        f.close()
        sftp.close()

        #return os.path.abspath(__filename__)
        return "test/myscript.sh"

    def test_submit_script(self,job_command, name,wwhoptions):
        sftp = self.ssh.open_sftp()
        filename = "myscript.sh"

        if os.path.isfile("test/"+filename): #todo:double check
            os.remove()
        else:
            try:
                sftp.mkdir('test')
            except IOError:
                pass
        f = sftp.open('test' + '/' + filename, 'w')
        f.write("#!/bin/bash")
        f.write('\n')
        f.write(job_command)
        f.close()
        sftp.close()

        #return os.path.abspath(__filename__)
        return "test/myscript.sh"

    def run_job_cmd(self,command, script_name):
        """ submit job as command
            Keyword arguments:
            command -- (qsub) command to execute, string
            script_name -- script, string
            Returns:
            jobid = JOB_ID for submitted job, string
        """
        jobid = '0'
        command = command + " " + script_name
        #print '\n command is ', command
        try:
            stdin, stdout, stderr =self.ssh.exec_command(command)
            outputString = str(stdout.read())
            if 'ERROR' in outputString:
                self.error_log += "\nerror in job command execution " + outputString
            else:
                jobid = self.get_jobid(outputString)

        except:
                self.error_log += "\n exception in job command submission " + str(sys.exc_info()[0])
        return jobid

    def get_jobid(self, str):
        """ get JOB_ID
            Keyword arguments:
            str - output string sent to the screen by qsub command
            Returns:
            JOB_ID as string
        """
        return str.split()[2]

    def get_status(self, userid, jobid):
        """ Get job status
            Keyword arguments:
            jobid - JOB_ID, string
            Returns:
            outputString - output sent to the screen when job status is checked.
                          If no output, returns 'completed'
        """
        status = ''
        try:
            #command = "qstat -j " + str(jobid)
            command = "qstat -u " + str(userid) + " | " + " grep " + jobid # qstat -u netid | grep jobid
            stdin, stdout, stderr = self.ssh.exec_command(command)
            outputString = str(stdout.read())

            if int(jobid) <> 0 and (outputString is None or len(outputString) == 0):
                status = 'completed'
                print '\n job is completed' # no output  if job is completed
            elif int(jobid) == 0:
                status = 'error in job submission'

            else:
                status_code = outputString.split()[4]
                status = self.get_status_code_report(status_code)

        except:
             self.error_log += "\n exception in job status " +str(sys.exc_info()[0])
        return status

    def get_file(self, remotepath, localpath):
        """ Copy file from remote to local
            Keyword arguments:
            remotepath -- path to remote file, string
            localpath -- path to local file, string
        """

        ftp = self.ssh.open_sftp()
        try:
            ftp.get(remotepath, localpath)
        except:
            self.error_log += "Error in get_file " +str(sys.exc_info()[0])
        ftp.close()

    def put_file(self, localpath, remotepath):
        """ Copy file from local to remote
           Keyword arguments:
           remotepath -- path to remote file, string
           localpath -- path to local file, string
        """

        sftp = self.ssh.open_sftp()
        sftp.put(localpath, remotepath)
        sftp.close()

    def get_status_code_report(self,code):
        if code == 'r':
            return 'running'
        elif code == 'q':
            return 'queued'
        elif code == 'e':
            return 'error'
        elif code == 'h':
            return 'hold'
        elif code =='w':
            return 'waiting'
        elif code == 'T':
            return 'reached the limit of the tail'
        elif code == 'S':
            return 'Suspended by the queue'
        elif code == 's':
            return 'suspended'
        #restarting?
        elif code == 'qw':
            return 'queued and waiting'
        else:
            return code

    def get_error_log(self):
        return  self.error_log

if __name__ == '__main__':

    hpcm = HPCJobManager()
    hpcm.connect('/vagrant/mtc/blast/config/hpc.config')

    #jobid = hpcm.submit("/afs/crc.nd.edu/user/a/aalber1/blast/4_blast_script.sh nt.fsa",None,None, None,{'-N':'tuesday7.out'})
    #print '\n jobid is ', jobid
    #status = hpcm.get_status('aalber1',jobid)
    #print '\n status is ', status
    #hpcm.put_file('/vagrant/mtc/blast/models.py', 'blast/models.py')
    jobid = hpcm.submit_cmd("~/blast/ncbi-blast-2.2.31+/bin/blastn -db ~/blast/aedes_db -query ~/blast/nt.fsa -out ~/blast/results_mtaedes.out","../hpcmanager/config/qsub.config", options={'-N':'thursday2.out'})
    print '\n jobid is ', jobid
    #todo: get file names, status, submit
    #hpcm.get_file("blast/results_taedes_353828.out","/vagrant/mtc/results_taedes_353828.out")
    print hpcm.get_error_log()
    hpcm.disconnect()