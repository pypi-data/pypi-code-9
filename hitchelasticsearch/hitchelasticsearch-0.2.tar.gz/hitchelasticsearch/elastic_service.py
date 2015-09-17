from hitchtest.environment import checks
from hitchserve import Service
from os.path import join
import signal
import shutil
import sys

class ElasticService(Service):
    def __init__(self, elastic_package, **kwargs):
        self.elastic_package = elastic_package
        checks.freeports([9200, 9300, ])
        kwargs['command'] = [elastic_package.elasticsearch, ]
        kwargs['log_line_ready_checker'] = lambda line: "started" in line
        kwargs['no_libfaketime'] = True
        super(ElasticService, self).__init__(**kwargs)
