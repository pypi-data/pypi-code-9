import sys

__author__ = 'drews'

PY_VERSION = sys.version_info[:2]
PY2 = (PY_VERSION[0] == 2)
PY3 = (PY_VERSION[0] == 3)


class Vagrantfile(object):
    def __init__(self):
        self.struct = BaseObject()

    def __getattr__(self, name):
        return getattr(self.struct, name)


class BaseObject(object): pass


class VagrantfileVm(object): pass


class VagrantfileProviderVb(object): pass


class VagrantfileProvisionShell(object): pass


class VagrantfileProvisionChef(object):
    def __init__(self):
        self.roles = []
        self.recipes = []

    def add_recipe(self, new_recipe):
        self.recipes.append(new_recipe)

    def add_role(self, new_role):
        self.roles.append(new_role)


class VagrantfileProvisionPuppet(object): pass


class VagrantfileNetworkForwardedPort(object):
    def __init__(self, guest, host):
        self.guest = int(guest)
        self.host = int(host)


class VagrantfileNetworkPrivateNetwork(object):
    def __init__(self, ip=None):
        self.ip = ip
