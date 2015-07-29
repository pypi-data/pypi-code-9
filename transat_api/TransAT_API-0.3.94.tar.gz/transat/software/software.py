"""
Generic class to describe software packages

"""


class Software(object):
    """

    """

    def __init__(self, name, actions=[]):
        """Software program

        Each program exposes a list of actions that can be executed

        Args:
            name (str): Name of the software program
            actions (list of str): List of actions that can be executed

        """
        self.name = name
        self.actions = actions
        self.installations = {}

    def set_installations(self, installations):
        self.installations = installations

    def add_action(self, action):
        if action not in self.actions:
            self.actions.append(action)

    def add_installation(self, installation):
        self.installations[installation.worker.name] = installation

    def run(self, action, worker_name, args):
        installation = self.get_installation(worker_name)
        return installation.run(action, args)

    def get_installation(self, worker_name):
        return self.installations[worker_name]
