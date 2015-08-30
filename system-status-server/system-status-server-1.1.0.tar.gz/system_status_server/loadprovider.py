
import os

from system_status_server.dataproviderbase import DataProviderBase

class LoadProvider(DataProviderBase):

    def fetch(self):

        return dict(
            load = os.getloadavg()
        )
