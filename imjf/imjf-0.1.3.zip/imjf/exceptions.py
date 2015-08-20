
class IMJFException(Exception):
    pass

class ReportException(IMJFException):
    def __init__(self, report):
        self.data = report
        IMJFException.__init__(self, self._message())

    def _message(self):
        defaultmessage = 'Something went wrong'

        try:
            return self.data.get('message', defaultmessage)
        except (AttributeError, TypeError):
            return defaultmessage
