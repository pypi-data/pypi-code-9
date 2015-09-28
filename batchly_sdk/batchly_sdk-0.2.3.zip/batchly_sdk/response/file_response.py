from iresponse import IResponse

class FileResponse(IResponse):
    """
        FileResponse is the type of response to return when you generate a file output
        Batchly Agent automatically takes the output file and sends it to the right destination(s)
        The destinations are configured from the portal and is processor independent
        Destinations are attached at the Job Level. The processor is reusable across many jobs without knowing the source and destination
    """

    def __init__(self, request, locations = None):
        self._locations = locations
        super(FileResponse, self).__init__(request)

    @property
    def locations(self):
        return self._locations

    @locations.setter
    def locations(self, value):
        """
            locations of the ouptut files on disk
            One full path per output file.  Disk File Name is used as file name for response.
            E.g.:- C:\Processed\Output\File1.png - Saved to storage as File.Png

            Type: Array
        """
        self._locations = value
