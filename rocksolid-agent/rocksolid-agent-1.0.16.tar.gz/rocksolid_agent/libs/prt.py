class PRT:
    def __init__(self, agent):
        from base import bcolors

        self.bcolors = bcolors
        self.agent   = agent

    def scan (self):
        import subprocess
        from base import module_exists

        self.agent.fb(1, 'Probing ports')
        #ports = os.popen('/bin/netstat -ntulp | grep :::').read()
        #ports = ports.split()

        if module_exists('subprocess'):
            out, err = subprocess.Popen(['/bin/netstat','-ntlp'], stdout=subprocess.PIPE).communicate()
            lines = out.splitlines()

            i = 0
            while i < len(lines):
                try:
                    ports = lines[i].split()
                    self.agent.fb(1, 'Found open port ' + ports[3] + ' (' + ports[0] + ' ' + ports[5] + ' ' + ports[6] + ')')
                except Exception, e:
                    pass
                i += 1
        results = []

        return results