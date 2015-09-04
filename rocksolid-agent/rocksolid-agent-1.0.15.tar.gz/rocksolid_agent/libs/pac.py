class PAC:
    def __init__(self, agent):
        from base import bcolors

        self.bcolors = bcolors
        self.agent   = agent

    def scan (self):
        import subprocess

        self.agent.fb(1, 'Scanning packages')

        #out, err = subprocess.Popen(['/bin/rpm','-qa'], stdout=subprocess.PIPE).communicate()
        #packages = out.splitlines()

        cmd = subprocess.Popen(["/bin/rpm", "-qa"], stdout=subprocess.PIPE)
        packagesraw, _ = cmd.communicate()
        packagesraw = packagesraw.rstrip()
        packages = packagesraw.split("\n")

        return packages