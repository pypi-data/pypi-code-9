# encoding=utf-8

import traceback
import logging as log
import json
import os

import tornado
import psutil

from rainbow.webhandler import ClusterWebHandler
from rainbow.wshandler import serverinfo
from rainbow.api import update_config


def process_info():
    pid = os.getpid()
    p = psutil.Process(pid)

    info = {'pid': pid,
            'cpu': p.cpu_percent(interval=0.1),
            'mem': '%.3f' % p.memory_percent(),
            }
    return info


class ServerInfoHandler(ClusterWebHandler):

    def prepare(self):
        self.need_sign = False
        return super(ClusterWebHandler, self).prepare()

    @tornado.web.asynchronous
    def get(self):
        try:
            self.cluster_init()
            if not self.get_query_argument('cluster', ''):
                self.cluster = False
                self.cluster_send_get(uri='/serverinfo/')
            else:
                self.cluster = True

            self.data = {}
            self.data['serverinfo'] = []

            data = serverinfo()
            data['status'] = 0
            data['process'] = process_info()
            self.handler_return(data)
        except Exception, e:
            self.exception_finish(e, traceback.format_exc())

    def handler_return(self, data):
        log.debug('ServerInfoHandler data = %s' % data)
        self.server_rsp_cnt = self.server_rsp_cnt + 1

        if self.cluster:
            self.data = data
        else:
            if data['status'] == 0:
                self.data['serverinfo'].append(data)

        if self.server_rsp_cnt == self.server_cnt:
            self.send_finish()

    def sort_by_host(self, item):
        return item['server']

    def send_finish(self):
        log.debug('self.data = %s' % self.data)
        try:
            if self.cluster:
                self.finish(json.dumps(self.data))
            else:
                self.data['serverinfo'] = sorted(
                    self.data['serverinfo'], key=self.sort_by_host)
                self.render('serverinfo.html', data=self.data)
        except Exception, e:
            self.exception_finish(e, traceback.format_exc())


class UpdateConfigHandler(ClusterWebHandler):

    """ 更新配置文件
    """

    def prepare(self):
        self.need_sign = False
        return super(ClusterWebHandler, self).prepare()

    @tornado.web.asynchronous
    def get(self):
        try:
            self.cluster_init()

            if not self.get_query_argument('cluster', ''):
                self.cluster_send_get(uri='/updateconfig/')

            update_config()

            data = {'status': 0}

            self.handler_return(data)
        except Exception, e:
            self.exception_finish(e, traceback.format_exc())
