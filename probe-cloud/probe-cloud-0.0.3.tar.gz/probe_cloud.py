#!/usr/bin/env python
from cleo import Command, InputArgument, InputOption
from cleo import Application
from probe.cloud import Cloud
import logging
import probe.log
import probe.rdirwatcher
import probe.cloud

class CheckCommand(Command):
    name = 'cloud:check'

    description = 'returns all compures where is AD running right now'

    options = [
        {
            'name': 'rdirwatcher_cfg',
            'description': 'path to rdirwatcher config file',
            'value_required': True,
            'default': 'rdirwatcher.cfg',
        }
    ]

    @staticmethod
    def execute(i, o):


        rdirwatcher_cfg = i.get_option('rdirwatcher_cfg')
        cloud = Cloud(rdirwatcher_cfg)

        cloud.check()

class RunSimulationCommand(Command):
    name = 'cloud:run_simulation'
    description = 'run simulation on cloud'

    options = [
        {
            'name': 'rdirwatcher_cfg',
            'description': 'path to rdirwatcher config file',
            'value_required': True,
            'default': 'rdirwatcher.cfg',
        }
    ]

    @staticmethod
    def execute(i, o):
        rdirwatcher_cfg = i.get_option('rdirwatcher_cfg')
        cloud = Cloud(rdirwatcher_cfg)
        cloud.run_simulation()



if __name__ == '__main__':

    logging.getLogger('paramiko').setLevel(logging.WARNING)
    logger = probe.log.get_logger('rdirwatcher')
    logger.setLevel(logging.DEBUG)
    probe.rdirwatcher.rdirwatcher.logger = logger
    probe.cloud.cloud.logger = logger

    application = Application()
    application.add(CheckCommand())
    application.add(RunSimulationCommand())
    application.run()
