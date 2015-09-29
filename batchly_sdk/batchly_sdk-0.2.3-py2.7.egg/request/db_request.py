from irequest import IRequest

class DbRequest(IRequest):
    """
          DbRequest is a type of request that supports relational data sources
          Request holds the base data and source connection string
    """
    def __init__(self, id, content_path, parameters, connection_string, data):
        self._connection_string = connection_string
        self._data = data
        super(DbRequest, self).__init__(id, content_path,parameters)

    @property
    def connection_string( self):
        """
            Connection string from where data was read.

            Type: String
        """
        return self._connection_string

    @property
    def data( self):
        """
            Dictionary of data that was retrieved for this unit of work

            Type: Dictionary
        """
        return self._data
