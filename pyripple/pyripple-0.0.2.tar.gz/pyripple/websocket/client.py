import json
import time

from ws4py.client import tornadoclient
import tornado


class WebSocketClientBase(tornadoclient.TornadoWebSocketClient):
    def __init__(self, url):
        tornadoclient.TornadoWebSocketClient.__init__(self, url)
        self.__keepAliveMgr = None
        self.__connected = False

    # This is to avoid a stack trace because TornadoWebSocketClient is not implementing _cleanup.
    def _cleanup(self):
        ret = None
        try:
            ret = tornadoclient.TornadoWebSocketClient._cleanup(self)
        except Exception:
            pass
        return ret

    def getIOLoop(self):
        return tornado.ioloop.IOLoop.instance()

    # Must be set before calling startClient().
    def setKeepAliveMgr(self, keepAliveMgr):
        if self.__keepAliveMgr is not None:
            raise Exception("KeepAliveMgr already set")
        self.__keepAliveMgr = keepAliveMgr

    def received_message(self, message):
        try:
            msg = json.loads(message.data)

            if self.__keepAliveMgr is not None:
                self.__keepAliveMgr.setAlive()
                if self.__keepAliveMgr.handleResponse(msg):
                    return

            self.onMessage(msg)
        except Exception, e:
            self.onUnhandledException(e)

    def opened(self):
        self.__connected = True
        if self.__keepAliveMgr is not None:
            self.__keepAliveMgr.start()
            self.__keepAliveMgr.setAlive()
        self.onOpened()

    def closed(self, code, reason=None):
        self.__connected = False
        if self.__keepAliveMgr:
            self.__keepAliveMgr.stop()
            self.__keepAliveMgr = None
        tornado.ioloop.IOLoop.instance().stop()

        self.onClosed(code, reason)

    def isConnected(self):
        return self.__connected

    def startClient(self):
        tornado.ioloop.IOLoop.instance().start()

    def stopClient(self):
        self.close_connection()

    ######################################################################
    # Overrides

    def onUnhandledException(self, exception):
        logger.critical("Unhandled exception", exc_info=exception)
        raise

    def onOpened(self):
        pass

    def onMessage(self, msg):
        raise NotImplementedError()

    def onClosed(self, code, reason):
        pass

    def onDisconnectionDetected(self):
        pass

