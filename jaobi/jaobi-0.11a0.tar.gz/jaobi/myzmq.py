# -*- coding: utf-8 -*-

import json
from pyrocumulus.converters import get_converter
from tornado import gen
import zmq
from zmq.eventloop import zmqstream
from zmq.eventloop.ioloop import ZMQIOLoop
from jaobi.models import ContentConsumption


class ZMQBase:

    def __init__(self, url, socket_type):
        self.url = url
        self.context = zmq.Context()
        self.socket = self.context.socket(socket_type)
        self.stream = None
        self.is_connected = False

    def connect(self):
        if not self.is_connected:
            loop = ZMQIOLoop()
            self.socket.bind(self.url)
            self.stream = zmqstream.ZMQStream(self.socket, loop)
            self.is_connected = True

    def disconnect(self):
        if self.is_connected:
            self.socket.disconnect(self.url)
            self.is_connected = False


class ZMQServer(ZMQBase):

    def __init__(self, url):
        super().__init__(url, zmq.PULL)

    def dict2obj(self, mydict, objtype):
        obj = objtype(**mydict)
        return obj

    def on_recv(self, multipart_message):
        message = ''.join([p.decode() for p in multipart_message])
        mydict = json.loads(message)
        obj = self.dict2obj(mydict, ContentConsumption)


class ZMQClient(ZMQBase):

    def __init__(self, url):
        super().__init__(url, zmq.PUSH)

    @gen.coroutine
    def obj2dict(self, obj):
        converter = get_converter(obj, max_depth=1)
        mydict = yield converter.to_dict()
        mydict = converter.sanitize_dict(mydict)

        return mydict

    @gen.coroutine
    def push(self, obj):
        obj = yield self.obj2dict(obj)
        myjson = json.dumps(obj)
        self.sender.send_json(myjson)
