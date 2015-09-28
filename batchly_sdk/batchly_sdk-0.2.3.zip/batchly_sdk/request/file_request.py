from irequest import IRequest

class FileRequest(IRequest):
    """
        Use this request if you require the file to be available on local disk for processing.
        You can access the input file location using the Location property
    """
    def __init__(self, id, content_path, parameters,location):
        self._location = location
        super(FileRequest, self).__init__(id, content_path,parameters)

    @property
    def location(self):
        """
            Location of input file on local disk.

            Type: String
        """
        return self._location
