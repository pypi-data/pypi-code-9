# -*- coding: utf-8 -*-

import os
import sys
import signal
import time
import websocket

from threading import Thread

from logger import get_logger
from config import Config
from utils import FileReader
from message import Message
from tools.timer import Timer
import editors

class AbsintheClient():

    def __init__(self, config, logger):
        self.config = config.raw()
        self.logger = logger

    def start(self):
        self.create_hosts(self.config['hosts'])
        self.create_editors(self.config['editors'])
        self.create_sessions(self.config['sessions'])

        for name in self.hosts:
            host = self.hosts[name]
            if len(host.on_connect_callbacks):
                host.connect()

        # a very simple blocking mecha...
        while True:
            try:
                sys.stdin.read(1)
            except KeyboardInterrupt as k:
                self.stop()
                break

    def create_sessions(self, sessions):
        self.logger.debug('Create sessions')
        self.sessions = {}
        for session in sessions:
            if session['enabled'] != True:
                continue
            name = session['name']
            if session['host'] not in self.hosts:
                self.logger.error('Undefined host %s in session %s. Ignoring session.' % (session['host'], name))
                continue

            if session['editor'] not in self.editors:
                self.logger.error('Undefined editor %s in session %s. Ignoring session.' % (session['editor'], name))
                continue

            self.sessions[name] = Session(name, self.hosts[session['host']], self.editors[session['editor']], session['path'], session['remote-path'], self.logger)

    def create_editors(self, editors_defs):
        self.logger.debug('Create editors')
        self.editors = {}
        for name in editors_defs:
            if not hasattr(editors, name):
                self.logger.error('Undefined editor: %s. Skipping.' % name)
                continue
            TypedEditor = getattr(editors, name)
            self.editors[name] = TypedEditor(name, editors_defs[name], self.logger)

    def create_hosts(self, hosts):
        self.logger.debug('Create hosts')
        self.hosts = {}
        for name in hosts:
            addr = hosts[name]
            self.hosts[name] = Host(name, addr['host'], addr['port'], self.logger)

    def stop(self):
        pass

class Host():
    def __init__(self, name, host, port, logger):
        self.msg_queue = []
        self.logger = logger
        self.name = name
        self.host = "ws://%s:%d" % (host, port)

        self.sessions = {}
        self.connected = False
        self.on_connect_callbacks = []

        self.reconnect_timer = Timer(10, self.connect)

    def connect(self):
        self.logger.debug('Try to connect to %s - %s' % (self.name, self.host))
        self.socket = websocket.WebSocketApp(self.host, on_message = self.on_message, on_error = self.on_error, on_close = self.on_close)
        self.socket.on_open = self.on_open

        th = Thread(target=self.socket.run_forever)
        th.setDaemon(True)
        th.start()

    def on_connect(self, callback):
        self.on_connect_callbacks.append(callback)

    def send(self, message):
        if not self.is_connected():
            self.logger.error('Try to send message, but no open socket. Name: %s, Message: %s' % (self.name, message))
            self.msg_queue.append(message)
            return

        self.logger.debug('Send message to %s: %s' % (self.host, message))

        self.socket.send(str(message))

    def is_connected(self):
        return self.connected

    def subscribe(self, name, session):
        if name not in self.sessions:
            self.sessions[name] = []

        self.sessions[name].append(session)

    def on_open(self, ws):
        self.connected = True
        self.reconnect_timer.stop()
        self.logger.info('Connected to %s - %s' % (self.name, self.host))

        for callback in self.on_connect_callbacks:
            callback()

        for msg in self.msg_queue:
            self.send(msg)
        self.msg_queue = []

    def on_message(self, ws, message):
        try:
            msg = Message.from_str(message)
        except Exception as e:
            self.logger.error('Malformed message received via websocket: %s, %s' % (e, message))
            return

        self.logger.debug('Message received %s' % msg)

        if msg.name not in self.sessions:
            self.logger.error('Unknown session %s' % msg.name)
            return

        for session in self.sessions[msg.name]:
            if hasattr(session, msg.command):
                func = getattr(session, msg.command)
                func(**msg.arguments)
            else:
                self.logger.error('Unknown command %s for session %s' % (msg.command, session.name))

    def on_error(self, ws, error):
        self.logger.error('Error occured on websocket: %s' % s)

    def on_close(self, reason):
        if self.is_connected():
            self.logger.error('%s socket closed, try to reconnect...' % self.name)
            self.connected = False
        self.reconnect_timer.start()

class Session():
    def __init__(self, name, host, editor, path, remote_path, logger):
        self.name = name
        self.host = host
        self.editor = editor
        self.path = path
        self.logger = logger
        self.remote_path = remote_path

        host.subscribe(name, self)
        host.on_connect(self.on_host_connected)

    def on_host_connected(self):
        msg = Message(self.name, 'session_start', dict(remote_path = self.remote_path))
        self.host.send(msg)

    def set_focus(self):
        self.editor.set_focus()

    def open_content(self, content):
        pass

    def open_file(self, filename, line = 1):

        full_path = os.path.join(self.path, *filename)

        self.logger.debug('Open file: %s' % full_path)

        self.editor.open_file(full_path, line)
