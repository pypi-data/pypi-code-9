

class ServiceManager(object):

    def __init__(self, cls, name, display_name = None):
        self.cls = cls

    def start(self):
        service = self.cls()
        service.start()

    def stop(self):
        pass

    def remove(self):
        pass

    def install(self, stay_alive=True):
        pass
