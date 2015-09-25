import websocket
import thread
import json
import handlers as h


class LoveMe:
    def __init__(self, apikey, device_id):
        self.apikey = apikey
        self.device_id = device_id
        ws = websocket.WebSocketApp('ws://localhost:8080/ws/' + apikey + '/' + device_id,
                                    on_message=self.on_message,
                                    on_error=self.on_error,
                                    on_close=self.on_close)
        ws.on_open = self.on_open
        self.ws = ws

    def on_message(self, ws, message):
        #print message
        self.handle_message(message)

    def on_error(self, ws, error):
        print error

    def on_close(self, ws):
        print "### connection closed ###"
        while True:
            try:
                thread.start_new_thread(self.ws.run_forever, ())
                break
            except ValueError:
                print "trying to reconnect"

    def on_open(self, ws):
        print 'opening connection'

    def deamonize(self):
        thread.start_new_thread(self.ws.run_forever, ())

    def send_message(self, message):
        self.ws.send(message)

    def handle_message(self, message):
        try:
            data = json.loads(message)
            print data
            if data:
                self.handle_message_type(data['type'], data)
            else:
                return {'status': 'error', 'message': 'data not found'}
        except Exception as e:
            print e.message
            return {'status': 'error', 'message': e.message}

    def handle_message_type(self, type, data):
        if type == 'gpio':
            self.send_message(json.dumps({'results': h.gpio_handler(data)}))
        elif type == 'pwm':
            self.send_message(json.dumps({'results': h.pwm_handler(data)}))
        elif type == 'ssh':
            self.send_message(json.dumps({'results': h.ssh_handler(data)}))
        elif type == 'camera':
            h.camera_handler(data)
        else:
            print "wrong command"