# -*- coding: utf-8 -*-
import os

from celery import Celery

class WorkerConnect(object):

    @classmethod
    def __init__(self, broker_url=os.environ.get('WORKER_BROKER_URL'), backend_url=os.environ.get('WORKER_BACKEND_URL')):

        if hasattr(self,'celery') is False:
            self.celery = Celery('WorkerConnect', broker=broker_url, backend=backend_url)
        else:
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
            return { 'status': 'success', 'code': 200, 'data': celery_response }
        else:
            celery_response = self.celery.signature(task_name, kwargs=data).delay()

            if celery_response.status == 'SUCCESS' or celery_response.status == 'PENDING':
                return { 'status': 'success', 'code': 200 }
            else:
                return { 'status': 'success', 'code': 500 }