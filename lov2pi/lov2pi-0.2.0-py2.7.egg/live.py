import websocket


class Manage:
    def __init__(self, appkey):
        self.appkey = appkey
        websocket.enableTrace(True)
        ws = websocket.WebSocketApp("ws://localhost:8080/ws/device?appkey=" + appkey,
                            on_message=self.on_message,
                            on_error=self.on_error,
                            on_close=self.on_close)
        ws.on_open = self.on_open
        self.ws = ws

    def on_message(self, ws, message):
        print message

    def on_error(self, ws, error):
        print error

    def on_close(self, ws):
        print "### closed ###"

    def on_open(self, ws):
        print 'opening connection'

    def deamonize(self):
        self.ws.run_forever()
