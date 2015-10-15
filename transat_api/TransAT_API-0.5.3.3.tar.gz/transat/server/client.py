import requests
import time
from progressbar import Bar, ETA, Percentage, ProgressBar, ReverseBar, RotatingMarker

class Client(object):
    def __init__(self, address):
        self.address = address

    def run_init(self, wd, nprocs):

        r = requests.post(self.address, data={'wd': wd, 'nprocs': nprocs, 'fun': 'run_init'})


    def run(self, wd, nprocs):
        r = requests.post(self.address, data={'wd': wd, 'nprocs': nprocs, 'fun': 'run'})

    def stop(self):
        r = requests.post(self.address+"/stop")


    def get_remaining_time(self):
        """ get remaining simulation time in minute

        """
        r = requests.get(self.address + "/remainingTime")
        return r.json()['value']


    def get_current_iteration(self):
        """ get current iteration

        """

        r = requests.get(self.address + "/iteration")
        return float(r.json()['value'])


    def get_current_timestep(self):
        """ get current time step

        """

        r = requests.get(self.address + "/timestep")
        return r.json()['value']

    def get_stdout(self):
        pass

    def is_running(self):
        r = requests.get(self.address + "/running")
        return r.json()['value']


    def has_jobs(self):
        r = requests.get(self.address + "/jobs")
        return r.json()['value']


    def watch(self, nbr_iterations=None):
        try:
            widgets = ['Simulation: ', Percentage(), ' ', Bar(marker=RotatingMarker()),
               ' ', ETA(), ' ']
            pbar = ProgressBar(widgets=widgets, maxval=10000).start()
            start = time.time()
            remaining = 0.0
            while self.has_jobs():
                elapsed = (time.time() - start)

                if nbr_iterations is not None:
                  current_iteration = self.get_current_iteration()
                  remaining = nbr_iterations-current_iteration
                  if current_iteration != 0:
                      remaining = remaining/current_iteration*elapsed
                else:
                  remaining = self.get_remaining_time()*60.0
                percentage = elapsed/(elapsed+remaining)*10000
                pbar.update(percentage)
                time.sleep(1)
            pbar.finish()
        except KeyboardInterrupt:
            #print "Keyboard Interrupt"
            #print "Sending stop signal to server"
            #self.stop()
            #while(self.is_running()):
            #    time.sleep(1)
            raise
