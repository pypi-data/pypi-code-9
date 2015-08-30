
import psutil

from system_status_server.dataproviderbase import DataProviderBase

class CPUProvider(DataProviderBase):

    def fetch(self):

        return dict(
            cpu = dict(
                cores = psutil.cpu_count()
            )
        )
