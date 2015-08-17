""" Provide exam-focused system information and uid's
"""

import platform
import uuid

class SystemInfo(object):
    def __init__(self):
        self.node = platform.node()
        self.summary = "%s\n%s\n%s\n%s\n%s\n%s" % (
                                      platform.system(),
                                      platform.node(),
                                      platform.release(),
                                      platform.version(),
                                      platform.machine(),
                                      platform.processor()
                                     )
    
        # This includes the mac address. Watch out for multiple network
        # adapters.
        self.summary += "\n%s" % uuid.uuid1()

