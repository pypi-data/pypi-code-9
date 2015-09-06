
import time

class Service(object):

    # to be overridden
    def start(self):
        pass

    # to be overridden
    def stop(self):
        pass

    def log(self, msg):
        pass

    def sleep(self, sec):
        time.sleep(sec)
