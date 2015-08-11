import requests


class Client(object):
    def __init__(self, address):
        self.address = address

    def run_init(self, wd, nprocs):
        r = requests.post(self.address, data={'wd': wd, 'nprocs': nprocs, 'fun': 'run_init'})


    def run(self, wd, nprocs):
        r = requests.post(self.address, data={'wd': wd, 'nprocs': nprocs, 'fun': 'run'})

    def stop(self):
        pass

    def get_current_iteration(self):
        r = requests.get(self.address + "/iteration")
        return r.json()['value']


    def get_current_timestep(self):
        r = requests.get(self.address + "/timestep")
        return r.json()['value']

    def get_stdout(self):
        pass

    def has_jobs(self):
        r = requests.get(self.address + "/jobs")
        return r.json()['value']
