import logging
from intogen.config import get_config
from intogen.qc.quality_control import QualityControl


class IntogenTask(object):
    def __init__(self):
        # load all configuration
        config = get_config()
        self._exec_config = config.get_bulk_config(
            self.get_configuration_definitions().keys()
        )
        if len(self._exec_config.keys()) == 0:
            logging.info("CONF no configuration neeeded for this task")

        # Quality control
        self.qc = QualityControl()

    @staticmethod
    def get_configuration_definitions():
        """
        Returns a dictionary with the needed configuration keys and validation+default values
        e.g.
        {
            "some_configuration" : "boolean(default=True)"
        }
        :return: dict
        """
        raise NotImplementedError("Method has to be implemented and overridden")


    @staticmethod
    def get_configuration_filename():
        return "system.conf"

    def run(self):
        raise NotImplementedError("Method has to be implemented and overridden")

    def quality_control(self, entity: str, label: str, value, **kwargs):
        self.qc.report(entity, label, value, **kwargs)

    def get_exec_config(self):
        return self._exec_config


