"""

"""
import json
import os
from enum import Enum
import requests
import time
from . import settings


class Status(Enum):
    """

    """
    pending = 'pending'
    done = 'done'
    failed = 'failed'


class Action(Enum):
    """

    """
    store = 'store'
    process = 'process'


class ApplauseBuilds(object):
    """
    Build Upload Service API wrapper.
    """

    def __init__(self, session):
        self.session = session

    def get_upload_info(self, action, workflow, name):
        """
        Generates a BUAPS specific upload URL + hosting specific upload data
        to be forwared later on.

        :param action:
        :param workflow:
        :param name:
        :return:
        """
        resp = self.session.post(settings.BUAPS_STORE_URL, data={
            'action': action,
            'workflows': json.dumps(workflow),
            'original_name': name,
            # S3 rejects our requests if they contain Applause access_token. The redirect
            # back to BUAPS might end up requiring it.
            'redirect': 'none',
        })
        resp.raise_for_status()
        return resp.json()

    def upload_file(self, url, data, path):
        """

        :param url:
        :param data:
        :param path:
        :return:
        """
        files = {'file': open(path, 'rb')}
        requests.post(url=url, files=files, data=data).raise_for_status()

    def get_upload_status(self, token):
        resp = self.session.get(settings.BUAPS_STATUS_URL.format(token=token))
        resp.raise_for_status()
        return resp.json()

    def process_build(self, path, input_data):
        _, name = os.path.split(path)
        input_data = input_data or {}
        workflow = {
            'basic': {
                'original_name': name
            }
        }
        workflow["basic"].update(input_data)

        upload_data = self.get_upload_info(
            action=Action.process.name,
            workflow=workflow,
            name=name,
        )

        token = upload_data['token']
        url = upload_data['url']
        data = upload_data['data']

        self.upload_file(url=url, data=data, path=path)
        self.trigger_processing(token)

        status = Status.pending.name
        while status == Status.pending.name:
            data = self.get_upload_status(token)
            status = data['status']
            # TODO: Limit number of retries
            time.sleep(2)

        return token

    def trigger_processing(self, token):
        self.session.get(settings.BUAPS_SUCCESS_URL.format(token=token)).raise_for_status()
