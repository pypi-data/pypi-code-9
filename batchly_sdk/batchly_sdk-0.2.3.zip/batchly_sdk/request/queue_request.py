from irequest import IRequest

class QueueRequest(IRequest):
    """
        QueueRequest is a type of request that supports pub/sub or queue sources
        Request holds the content of a single message
    """

    def __init__(self, id, content_path, parameters, content):
        self._content = content
        super(QueueRequest, self).__init__(id, content_path,parameters)

    @property
    def content(self):
        """
            Message content.

            Type: String
        """
        return self._content
