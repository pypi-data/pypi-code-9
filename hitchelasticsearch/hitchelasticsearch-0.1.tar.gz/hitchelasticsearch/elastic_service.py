from hitchserve import Service
from os.path import join
import signal
import shutil
import sys

class ElasticService(Service):
    def __init__(self, elastic_package, **kwargs):
        self.elastic_package = elastic_package
        kwargs['command'] = [elastic_package.elasticsearch, ]
        kwargs['log_line_ready_checker'] = lambda line: "loaded" in line
        super(ElasticService, self).__init__(**kwargs)
