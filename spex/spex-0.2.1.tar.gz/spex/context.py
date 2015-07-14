import os
import sys
import json
from spex.utils import print_banner, ArtifactResolver

try:
    import py4j  # noqa
    from pyspark import SparkConf, SparkContext, SQLContext, HiveContext
except ImportError:
    raise ImportError('You attempted to import the spex.context module '
                      '_before_ the sys.path was fixed up for spark')

from .config import SpexConfig

# This is a singleton that will only exist within a single process, we reuse the context where it exists
# and recreate it in subprocesses where it does not exist
_SPARK_CONTEXT = None


_STARTUP_SCRIPT = '''
try:
    from spex.context import current
    spex_context = current()
except ImportError:
    import sys
    sys.path = %(path)s
    from spex.context import current
    spex_context = current("""%(context)s""")
sc = spex_context.sc
sql_ctx = spex_context.sql_ctx
del current
'''


class SpexContext(object):

    def __init__(self, spex_conf, artifact_resolver):
        global _SPARK_CONTEXT  # noqa
        assert _SPARK_CONTEXT is None, "Cannot have two spark contexts at once in the same process"
        _SPARK_CONTEXT = self

        self.spex_conf = spex_conf
        self.artifact_resolver = artifact_resolver

        os.environ['PYSPARK_PYTHON'] = './%s.spex' % spex_conf.spex_name

        self._spark_config = None
        self._spex_startup = None
        self._spark_context = None
        self._sql_context = None

    @property
    def sc(self):  # noqa
        if not self._spark_context:
            spark_context = SparkContext(conf=self.spark_config)

            assert self.spex_conf.spex_file is not None, "The spex builder must be broken I do not know my spex conf!"
            spark_context.addFile(self.spex_conf.spex_file)

            for py_file in self.spex_conf.spark_config.py_files:
                spark_context.addPyFile(py_file)

            for file in self.spex_conf.spark_config.files:  # noqa
                spark_context.addFile(file)

            for jar in self.spex_conf.spark_config.jars:  # noqa
                spark_context.addFile(jar)

            self._spark_context = spark_context
            print_banner(self)
        return self._spark_context

    @property
    def sql_ctx(self):
        if not self._sql_context:
            spark_context = self.sc
            try:
                # Try to access HiveConf, it will raise exception if Hive is not added
                spark_context._jvm.org.apache.hadoop.hive.conf.HiveConf()  # noqa
                self._sql_context = HiveContext(spark_context)
            except py4j.protocol.Py4JError:
                self._sql_context = SQLContext(spark_context)
        return self._sql_context

    @property
    def spark_config(self):
        if self._spark_config is None:
            os.environ['SPARK_SUBMIT_CLASSPATH'] = ','.join(self.spex_conf.spark_config.jars)

            conf = SparkConf()
            conf.setAppName(self.spex_conf.spark_config.name)
            conf.setMaster(self.spex_conf.spark_config.master)

            conf.set('spark.rdd.compress', 'true')
            conf.set('spark.io.compression.codec', 'lz4')
            conf.set('spark.mesos.coarse',
                     'true' if self.spex_conf.spark_config.coarse_mode else 'false')

            # TODO - Setup all the other cruft as needed
            #conf.set('spark.executor.memory', '4g')
            #conf.set('spark.cores.max', '16')
            #conf.set('spark.task.cpus', '6')

            # TODO - bind port for spark web ui

            self._spark_config = conf

        config = self._spark_config

        # These are always set, if someone changes them we simply set them back
        config.set('spark.executor.uri', self.artifact_resolver(self.spex_conf.spark_distro))
        config.setExecutorEnv(key='PYSPARK_PYTHON', value='./%s daemon' % self.spex_conf.spex_name)
        return config

    @property
    def startup_script(self):
        if self._spex_startup is None:
            spex_startup = os.path.join(self.spex_conf.spex_root, 'spex_startup.py')
            with open(spex_startup, 'w') as startup_script:
                startup_script.write(_STARTUP_SCRIPT % dict(path=sys.path, context=self.dumps()))
            self._spex_startup = spex_startup
        return self._spex_startup

    def dumps(self):
        return json.dumps({
            'spex_conf': self.spex_conf.to_dict(),
            'artifact_resolver': self.artifact_resolver.to_dict(),
            'sys.path': sys.path,
        })

    @classmethod
    def loads(cls, raw_data):
        data = json.loads(raw_data)
        spex_conf = SpexConfig.from_dict(data['spex_conf'])
        artifact_resolver = ArtifactResolver.from_dict(data['artifact_resolver'])
        return cls(spex_conf, artifact_resolver)

    def __enter__(self):
        return self

    def __exit__(self, _exc_type, _exc_val, _exc_tb):
        # Do not use self.sc, as that will hydrate the spark context
        # The entry_point can choose to do that itself
        if self._spark_context:
            self._spark_context.stop()


def current(serialised_context=None):
    global _SPARK_CONTEXT  # noqa
    if _SPARK_CONTEXT:
        return _SPARK_CONTEXT

    if serialised_context:
        return SpexContext.loads(serialised_context)

    return None

