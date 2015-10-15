#!/usr/bin/env python

from cleo import Command, InputArgument, InputOption
from cleo import Application
from probe.params import SimParams

class PrintParamsCommand(Command):
    name = 'params:print'

    description = 'loads an input.params file and print all parameters'

    arguments = [
        {
            'name': 'input',
            'description': 'path to input.params file',
            'required': True
        }
    ]

    options = [
        {
            'name': 'debye_fraction_user',
            'shortcut': 'f',
            'description': 'integer, how many grid points per one Debye length',
            'value_required': True,
            'default': None,
        }
    ]

    @staticmethod
    def execute(i, o):
        input_arg = i.get_argument('input')
        debye_fraction_user = i.get_option('debye_fraction_user')
        if debye_fraction_user:
            debye_fraction_user = int(debye_fraction_user)

        sp = SimParams(input_arg, debye_fraction_user=debye_fraction_user)

        sp.print_params('params')
        sp.print_sparams('sparams')
        sp.print_cparams('cparams')

if __name__ == '__main__':
    application = Application()
    application.add(PrintParamsCommand())
    application.run()
