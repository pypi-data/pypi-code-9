import sys
import logging

"""
Utility to help build Python applications using TransAT API
"""

LOG_FILE = 'transat_api.log'
logging.basicConfig(format='%(asctime)s %(levelname)s %(name)s  %(message)s',
                    filename=LOG_FILE, level=logging.DEBUG, filemode='w')


class Inputs(list):
    def __init__(self):
        super(Inputs, self).__init__()

    def add(self, name, **kwargs):
        """Add input

        Extended description of function.

        Args:
            name (int): Description of arg1
            kwargs (dict): Description of arg2

        Returns:
            bool: Description of return value

        """
        inp = {"name": name}
        inp.update(kwargs)
        self.append(inp)


class Outputs(list):
    def __init__(self):
        super(Outputs, self).__init__()

    def add(self, name, **kwargs):
        """Add output

        Extended description of function.

        Args:
            arg1 (int): Description of arg1
            arg2 (str): Description of arg2

        Returns:
            bool: Description of return value

        """
        inp = {"name": name}
        inp.update(kwargs)
        self.append(inp)


class App(object):
    def __init__(self, title):
        self.title = title
        self.inputs = Inputs()
        self.outputs = Outputs()
        self.func = lambda _: "Default function - overide me!"

    def add_input(self, name, **kwargs):
        """Define an input for the application

        Extended description of function.

        Args:
            name (str): Description of arg1
            kwargs (dict): Description of arg2

        Returns:
            bool: Description of return value

        """
        self.inputs.add(name, **kwargs)

    def add_output(self, name, **kwargs):
        """Define output of application

        Extended description of function.

        Args:
            name (name): Description of arg1
            kwargs (dict): Description of arg2

        Returns:
            bool: Description of return value

        """
        self.outputs.add(name, **kwargs)

    def add_main(self, func):
        """Summary line.

        Extended description of function.

        Args:
            arg1 (int): Description of arg1
            arg2 (str): Description of arg2

        Returns:
            bool: Description of return value

        """
        self.func = func

    def run(self, *args, **kwargs):
        """Summary line.

        Extended description of function.

        Args:
            arg1 (int): Description of arg1
            arg2 (str): Description of arg2

        Returns:
            bool: Description of return value

        """
        self._check_inputs()
        self.func(*args, **kwargs)
        logging.info("done with running")

    def _check_inputs(self):
        # TODO
        pass

    def set_server(self, url):
        pass

    def parse_inputs(self):
        """Summary line.

        Extended description of function.

        Args:
            arg1 (int): Description of arg1
            arg2 (str): Description of arg2

        Returns:
            bool: Description of return value

        """
        import argparse

        parser = argparse.ArgumentParser()
        for inp in self.inputs:
            name = inp['name']
            help_msg = [name]
            for key in inp:
                if key is not 'name':
                    help_msg.append('[' + str(key) + ']')
            if 'type' not in inp or inp['type'] is not 'Coupled':
                parser.add_argument('--' + name,
                                    dest=name,
                                    required=True,
                                    help=' '.join(help_msg))
        args = parser.parse_args()
        return vars(args)
