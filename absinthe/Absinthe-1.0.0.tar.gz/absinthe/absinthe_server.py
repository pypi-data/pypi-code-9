
import threading
import pyjsonrpc
import json
import os
from geventwebsocket import WebSocketServer, WebSocketApplication, Resource

from absinthe.tools.commands import CommandRequestHandler, external_jsonrpc_command
from absinthe.message import Message
from absinthe.tools.utils import SimpleResponse
from absinthe.tools.remote_process_base import RemoteProcessBase

# gevent socket in thread, need to patch...
from gevent import monkey
monkey.patch_all()

class Client(WebSocketApplication):
    def __init__(self, ws, manager):
        WebSocketApplication.__init__(self, ws)
        self.manager = manager
        self.address = '%(REMOTE_ADDR)s:%(REMOTE_PORT)s' % ws.environ

    def send(self, message):
        self.ws.send(str(message))

    def on_open(self):
        pass

    def on_message(self, message):
        if message is None:
            return
        self.manager.on_message(message, self)

    def on_close(self, reason):
        self.manager.on_close(self)

class Session(object):
    def __init__(self, name, client, path):
        self.name = name
        self.client = client
        self.path = path

class PathHandler(object):
    def __init__(self, name, path):
        self.name = name
        self.path = path

    def parse(self, filename):
        if filename.find(self.path) != 0:
            raise Exception('Path mismatch')

        fn = filename[len(self.path):]

        return fn.split(os.sep)

class ClientManager(object):
    def __init__(self, session_manager):
        self.session_manager = session_manager

    def __call__(self, ws):
        return Client(ws, self.session_manager)

class SessionManager(object):
    def __init__(self, logger):
        self.logger = logger
        self.sessions = {}
        self.paths = {}

    def register_path(self, path):
        self.paths[path.name] = path

    def find_sessions(self, path_name):
        sessions = []
        for name in self.sessions:
            for session in self.sessions[name]:
                if session.path.name == path_name:
                    sessions.append(session)
        return sessions

    @external_jsonrpc_command
    def set_focus(self, path_name):
        sessions = self.find_sessions(path_name)

        for session in sessions:
            session.client.send(Message(session.name, 'set_focus'))

        return SimpleResponse(True)

    @external_jsonrpc_command
    def open_file(self, path_name, filename, line):
        self.logger.debug('Open file %s in %s' % (path_name, filename))

        msgs = []

        try:
            sessions = self.find_sessions(path_name)

            if len(sessions) == 0:
                msg = 'There is no client for this path %s' % path_name
                self.logger.warning(msg)
                return SimpleResponse(False, [msg])

            msgs.append('Session found: %s' % path_name)

            for session in sessions:
                file_parts = session.path.parse(filename)
                session.client.send(Message(session.name, 'open_file', dict(filename = file_parts, line = line)))
                msgs.append('File open request sent to %s' % session.client.address)

            for msg in msgs:
                self.logger.debug(msg)

        except Exception as e:
            self.logger.exception(e);
            msgs.append(e);

        return SimpleResponse(True, msgs)

    def on_message(self, message, client):
        try:
            msg = Message.from_str(message)
        except Exception as e:
            self.logger.error('Malformed message received via websocket: %s, %s' % (e, message))
            return

        if hasattr(self, msg.command):
           func = getattr(self, msg.command)
           func(msg.name, client, **msg.arguments)
        else:
            self.logger.warning('Undefined command received: %s' % msg.command)

    def on_close(self, client):
        for name in self.sessions:
            for session in self.sessions[name]:
                if session.client == client:
                    self.sessions[name].remove(session)
                    self.logger.info('Session close: %s from %s' % (name, client.address))

    def session_start(self, name, client, remote_path):
        self.logger.info('Session start: %s from %s' % (name, client.address))
        session = Session(name, client, self.paths[remote_path])
        if name not in self.sessions:
            self.sessions[name] = []

        self.sessions[name].append(session)

class AbsintheServer(RemoteProcessBase):

    def __init__(self, config, logger):
        self.logger = logger
        self.config = config
        self.session_manager = SessionManager(self.logger)
        self.client_manager = ClientManager(self.session_manager)

    @external_jsonrpc_command
    def init(self):
        for name in self.config.data['paths']:
            self.session_manager.register_path(PathHandler(name, self.config.data['paths'][name].value))

        server_address = self.config.data['agent_server']
        self.server = WebSocketServer((server_address['host'].value, server_address['port'].value), Resource({'/': self.client_manager}))

        th = threading.Thread(target=self.server.serve_forever)
        th.setDaemon(True)
        th.start()

        self.logger.debug('init')

        return SimpleResponse(True)

    # Initialize the command server to receive IPC commands.
    def start_command_server(self):
        try:
            command_server_address = self.config.data['command_server']
            self.command_server = pyjsonrpc.ThreadingHttpServer(
                server_address = (command_server_address['host'].value, command_server_address['port'].value),
                RequestHandlerClass = CommandRequestHandler
            )
        except Exception as e:
            self.logger.error('Exception occured during the command server initalization: ' + str(e) + traceback.format_exc())
            return

        CommandRequestHandler.logger = self.logger
        CommandRequestHandler.externals.extend([self, self.session_manager])

        self.logger.debug('command server starting...')

        self.command_server.serve_forever()
