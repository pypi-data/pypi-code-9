import sys
import zmq


class AnalystRemoteControl(object):
    def __init__(self, sub_uri, req_uri):
        self.sub_uri = sub_uri
        self.req_uri = req_uri
        self.ctx = zmq.Context.instance()
        self.sub_sock = zmq.Socket(self.ctx, zmq.SUB)
        self.sub_sock.setsockopt(zmq.SUBSCRIBE, '')
        self.sub_sock.connect(self.sub_uri)
        self._acquire_requested = False
        self._acquire_started = False
        self._acquire_completed = False
        self.reset()

    def reset(self):
        self._command('Connect')
        self._command('QueueConnect')
        self._command('Ready')
        self._command('StopAcquisition')
        self._command('StopQueue')

    def _command(self, command):
        req_sock = zmq.Socket(self.ctx, zmq.REQ)
        req_sock.connect(self.req_uri)
        req_sock.send(command)
        response_code, result = req_sock.recv().split(':')
        if response_code != 'OK':
            raise IOError('%s: %s' % (response_code, result))
        else:
            return result

    def start_acquisition(self):
        self._command('StartAcquisition')
        self._acquire_started = False
        self._acquire_completed = False
        self._acquire_requested = True

    def acquisition_complete(self):
        while True:
            try:
                state = self.sub_sock.recv(zmq.NOBLOCK)
                if self._acquire_requested and state == 'Acquiring':
                    self._acquire_started = True
                elif self._acquire_started and not state == 'Acquiring':
                    self._acquire_completed = True
            except zmq.ZMQError as e:
                if e.errno == zmq.EAGAIN:
                    # nothing to recv
                    break
                else:
                    raise
        return self._acquire_completed


if __name__ == '__main__':
    import sys

    remote = AnalystRemoteControl(sys.argv[1], sys.argv[2])
