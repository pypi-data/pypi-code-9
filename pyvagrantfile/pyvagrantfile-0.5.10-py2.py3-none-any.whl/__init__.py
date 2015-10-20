import sys

__author__ = 'drews'

PY_VERSION = sys.version_info[:2]
PY2 = (PY_VERSION[0] == 2)
PY3 = (PY_VERSION[0] == 3)


class BaseObject(object):
    serializable = []

    def _get_attributes(self, attributes):
        filtered_attributes = {}
        for key in attributes:
            if hasattr(self, key):
                filtered_attributes[key] = getattr(self, key)
        return filtered_attributes

    def to_dict_iter(self, keys, structure, collection_type=None):
        new_dict = {} if (collection_type is None) else collection_type()
        for attribute in keys:
            if collection_type in [list, dict]:
                if attribute in keys:
                    attribute_value = structure[attribute]
                else:
                    continue
            else:
                if hasattr(structure, attribute):
                    attribute_value = getattr(structure, attribute)
                else:
                    continue
            if collection_type is list:
                new_dict.append(self.to_dict_obj(attribute_value))
            else:
                new_dict[attribute] = self.to_dict_obj(attribute_value)
        return new_dict

    def to_dict_obj(self, attribute_value):
        if hasattr(attribute_value, 'to_dict'):
            return getattr(attribute_value, 'to_dict')()
        elif isinstance(attribute_value, dict):
            return self.to_dict_iter(attribute_value.keys(), attribute_value, collection_type=dict)
        elif isinstance(attribute_value, list):
            return self.to_dict_iter(range(len(attribute_value)), attribute_value, collection_type=list)
        else:
            return attribute_value

    def to_dict(self):
        return self.to_dict_iter(self.serializable, self)
        # new_dict = {}
        # for attribute in self.serializable:
        #     attribute_value = getattr(self, attribute)
        #     if hasattr(attribute_value, 'to_dict'):
        #         new_dict[attribute] = getattr(attribute_value, 'to_dict')()
        #     elif isinstance(attribute_value, dict):
        #         sub_dict = {}
        #     else:
        #         new_dict[attribute] = attribute_value
        # return new_dict


class Vagrantfile(BaseObject):
    def to_dict(self):
        return {
            'vm': self.vm.to_dict()
        }


class VagrantfileVm(BaseObject):
    serializable = ['box', 'box_check_update', 'network', 'provider', 'provision', 'synched_folder']


class VagrantfileProviderVb(BaseObject):
    serializable = ['gui', 'memory']
    def to_dict(self):
        return {
            'gui': bool(self.gui),
            'memory': self.memory
        }


class VagrantfileProvisionShell(BaseObject):
    serializable = ['inline']


class VagrantfileProvisionChef(BaseObject):
    serializable = ['cookbooks_path', 'data_bags_path', 'json', 'recipes', 'roles', 'roles_path', 'run_list']

    def __init__(self):
        self.roles = []
        self.recipes = []

    def add_recipe(self, new_recipe):
        self.recipes.append(new_recipe)

    def add_role(self, new_role):
        self.roles.append(new_role)


class VagrantfileProvisionPuppet(BaseObject): pass


class VagrantfileNetworkForwardedPort(BaseObject):
    serializable = ['guest', 'host']

    def __init__(self, guest, host):
        self.guest = int(guest)
        self.host = int(host)

    def to_dict(self): return {'guest': self.guest, 'host': self.host}


class VagrantfileNetworkPrivateNetwork(BaseObject):
    serializable = ['ip']
    def __init__(self, ip=None):
        self.ip = ip
