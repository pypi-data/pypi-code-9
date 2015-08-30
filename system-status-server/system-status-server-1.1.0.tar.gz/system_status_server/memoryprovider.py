
import psutil

from system_status_server.dataproviderbase import DataProviderBase

class MemoryProvider(DataProviderBase):

    def fetch(self):

        mem_data = psutil.virtual_memory()

        return dict(
            memory = dict(
                total = mem_data.total,
                available = mem_data.available,
                used = mem_data.used,
                percent = mem_data.percent,
                free = mem_data.free,
            )
        )
