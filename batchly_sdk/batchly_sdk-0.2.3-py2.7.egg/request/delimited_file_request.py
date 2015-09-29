from irequest import IRequest

class DelimitedFileRequest(IRequest):
    """
        DelimitedFileRequest is a type of request that supports csv and other delmited type of source files
        Request holds the fields as an array.  The fields are column values from a single row

    """

    def __init__(self, id, content_path, parameters, fields):
        self._fields = fields
        super(DelimitedFileRequest, self).__init__(id, content_path,parameters)

    @property
    def fields(self):
        """
            Fields contain the individual columns of a delimited row

            Type: Array
        """
        return self._fields
