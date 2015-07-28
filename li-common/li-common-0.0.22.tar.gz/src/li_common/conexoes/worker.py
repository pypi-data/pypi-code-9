# -*- coding: utf-8 -*-
from celery import Celery

import json


class WorkerConnect(object):

    @classmethod
    def __init__(self, broker_url=None, backend_url=None):

        if hasattr(self,'celery') is False:
            print 1
            self.celery = Celery('WorkerConnect', broker=broker_url, backend=backend_url)
        else:
            print 2
            pass

    def execute(self, task_name, option='delay', args=None):

        if args is not None:
            data = args
        else:
            data = None

        if not data:
            return { 'status': 'erro', 'code': 500, 'msg': 'no args' }

        if option == 'get':
            celery_response = self.celery.signature(task_name, kwargs=data).delay().get(timeout=60)
            data = json.loads(celery_response)
            return { 'status': 'success', 'code': 200, 'data': data }
        else:
            celery_response = self.celery.signature(task_name, kwargs=data).delay()

            if celery_response.status == 'SUCCESS' or celery_response.status == 'PENDING':
                return { 'status': 'success', 'code': 200 }
            else:
                return { 'status': 'success', 'code': 500 }