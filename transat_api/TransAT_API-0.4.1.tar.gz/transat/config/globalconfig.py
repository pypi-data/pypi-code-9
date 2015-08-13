"""
Store configuration of software programs and their installations

    Examples:

"""


class GlobalConfig(object):
    def __init__(self, installations, softwares, env):
        self.env = env
        self.softwares = softwares
        self._register_installations_to_softwares(installations)

    def get_software(self, software_name):
        for soft in self.softwares:
            if soft.name == software_name:
                return soft

    def get_worker(self, worker_name):
        for software in self.softwares:
            for name in software.installations.keys():
                if name == worker_name:
                    return software.installations[worker_name].worker
        return None


    def _register_installations_to_softwares(self, installations):
        for soft in self.softwares:
            soft_installations = {}
            for installation in installations:
                if installation.software == soft:
                    soft_installations[installation.worker.name] = installation
            soft.set_installations(soft_installations)

