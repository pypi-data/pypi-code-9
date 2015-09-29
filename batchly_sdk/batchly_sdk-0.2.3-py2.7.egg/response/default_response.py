from iresponse import IResponse

class DefaultResponse(IResponse):
    """
        Use this response type when no post processing is required to be done by
        Batchly. Creating this DefaultResponse automatically updates the success
        state of the response.

        For explicitly setting the success as False or for marking this request
        as a duplicate request, you can set the is_processing_success or is_duplicate
        properties with the appropriate values
    """
    def __init__(self, request):
        super(DefaultResponse, self).__init__(request)
