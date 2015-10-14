import time
import subprocess

try:
    import paramiko as pa

    pa.util.log_to_file('paramiko.log')
except:
    print "could not import paramiko"
    pa = None


class Communicator(object):
    """Handle remote command execution and data transfer between workers

    .. Note::
        Uses `Paramiko <http://www.paramiko.org>`_ python package

    """

    def __init__(self, host, username):
        self.pa = pa
        self.username = username
        self.host = host
        self.ssh = None

    def _connect(self):
        self.ssh = self.pa.SSHClient()
        self.ssh.set_missing_host_key_policy(self.pa.AutoAddPolicy())
        self.ssh.connect(self.host, username=self.username)

    def _exit(self):
        self.ssh.close()

    def run_cmd(self, cmd, wd):
        self._connect()
        cmd = 'cd ' + wd + ' ; ' + cmd
        stdin, stdout, stderr = self.ssh.exec_command(cmd)
        while not stdout.channel.exit_status_ready():
            time.sleep(0.1)
        output = stdout
        error = stderr
        status = stdout.channel.recv_exit_status()
        self._exit()

        return status, output, error

    def upload(self, local_path, remote_path):
        remote_path = self.host + ":" + remote_path
        cmd = ['rsync', '-a', '-q', '-ave', 'ssh', local_path + "/", remote_path]
        process = subprocess.call(cmd)
        return process

    def download(self, remote_path, local_path):
        remote_path = self.host + ":" + remote_path
        cmd = ['rsync', '-a', '-q', '-ave', 'ssh', remote_path + "/", local_path]
        process = subprocess.call(cmd)
        return process

    def rsync(self, src, dest):
        if src['worker'] == 'local':
            src_path = src['path']
            dest_path = self.host + ":" + dest['path']
            cmd = 'mkdir -p ' + dest['path']
            code, output, error = self.run_cmd(cmd, '')
        elif dest['worker'] == 'local':
            src_path = self.host + ":" + src['path']
            dest_path = dest['path']
        else:
            raise Exception("One of src or dest must be local, cannot transfer between remote workers")
        cmd = ['rsync', '-a', '-q', '-ave', 'ssh', src_path + "/", dest_path]
        process = subprocess.call(cmd)
        return process
