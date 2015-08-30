
import psutil
import time

from system_status_server.dataproviderbase import DataProviderBase

class UptimeProvider(DataProviderBase):

    def fetch(self):

        return dict(
            uptime = int(time.time() - psutil.boot_time())
        )
