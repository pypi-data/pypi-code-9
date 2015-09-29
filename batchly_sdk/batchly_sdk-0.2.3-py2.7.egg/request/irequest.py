import abc

class IRequest(object):
    __metaclass__ = abc.ABCMeta
    """
        IRequest is the base interface for all request types
        Use the actual implementations while duck typing - File, Delimited, Db or Queue
    """

    def __init__(self, id, content_path, parameters):
        self._id = id
        self._contentPath = content_path
        self._parameters = parameters

    @property
    def id(self):
        """
            Identifier for the unit of work.

            Type: String
        """
        return self._id

    @property
    def content_path(self):
        """
            Current working directory. An isoldated work area for processing.
            Maintain temporary data and output in this folder.

            Type: String
        """
        return self._contentPath

    @property
    def parameters(self):
        """
            Key-Value configuration data for processing. You can plan for a list of paramters for your code.
            Configure them in the portal and values can be updated for each execution.

            Type: Dictionary
        """
        return self._parameters
