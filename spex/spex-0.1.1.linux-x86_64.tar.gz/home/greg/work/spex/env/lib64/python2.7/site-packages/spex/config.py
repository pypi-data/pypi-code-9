import os
import json
from collections import namedtuple

class SpexConfig(namedtuple('spex_config', 'spex_name spark_config spex_root '
                                           'spex_file spex_conf spark_distro entry_point')):

    def dumps(self):
        return json.dumps(self.to_dict())

    def to_dict(self):
        return dict(
            spex_name=self.spex_name,
            spex_root=self.spex_root,
            spex_file=self.spex_file,
            spex_conf=self.spex_conf,
            spark_distro=self.spark_distro,
            entry_point=self.entry_point,
            spark_config=self.spark_config._asdict()
        )

    @classmethod
    def loads(cls, raw_data):
        data = json.loads(raw_data)
        return cls.from_dict(data)

    @classmethod
    def from_dict(cls, data):
        def _env_defaulted(name):
            value = data.get(name, None)
            if value is None:
                value = os.environ[name.upper()]
            return value

        return SpexConfig(
            spex_name=data.get('spex_name'),
            spex_root=_env_defaulted('spex_root'),
            spex_conf=_env_defaulted('spex_conf'),
            spex_file=_env_defaulted('spex_file'),
            spark_distro=data.get('spark_distro', None),
            entry_point=data.get('entry_point', None),
            spark_config=SparkConfig(**data.get('spark_config', {}))
        )

class SparkConfig(namedtuple('spark_config', 'files jars py_files master name conf executor_memory spark_home '
                                             'total_executor_cores verbose driver_memory coarse_mode '
                                             'task_cpus local_dir event_log python_mem_ratio')):

    def dumps(self):
        return json.dumps(self._asdict())

    @classmethod
    def loads(cls, raw_data):
        return cls(json.loads(raw_data))

def load_spex_config():
    """Load the spex configuration that is needed to run a spex application

    This configuration is created by the spex tool and included into spex applications, the bootstrapper adds
    additional information that is necessary for spex to run, but should not be poked by end users directly.

    Returns
    -------
    spex_conf : dict
        The dictionary containing the basic, core spex config
    """
    try:
        with open(os.environ['SPEX_CONF']) as raw_spex_conf:
            return SpexConfig.loads(raw_spex_conf.read())
    except NameError:
        print "Unable to continue without SPEX_CONF being set, how did you build this spex file ?"
