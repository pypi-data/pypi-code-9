from functions import *
from constants import *
from utils import jjoin

import json
import logging

#######################################################
# Init debug functions
#######################################################
def printList(x):
	return "\n".join(str(y) for y in x)

def printDict(x):
	return "\n".join(str(y) + "\n" + str(x[y]) for y in x)
########################################################
# Main function
########################################################
def run():

	logger = logging.getLogger("parser.init")
	try:
		ListConfigFile = detect_all_config_file()
		LogFormat = get_all_log_formats(ListConfigFile)
		LogPattern = convert_all_format_to_regex(LogFormat)
		LogAccess = get_all_access_logs(ListConfigFile)
		machine_id = get_server_ip()

		#####################################
		logger.debug("====== List Config File ======")
		logger.debug(printList(ListConfigFile))

		logger.debug("====== List Log Pattern ======")
		logger.debug(printDict(LogPattern))

		logger.debug("====== List Log Accesss ======")
		logger.debug(printList(LogAccess))

		logger.debug("====== Server IP  ======")
		logger.debug(machine_id)
		####################################
		
		return (machine_id, LogAccess, LogPattern, ListConfigFile)
	except Exception, e:
		logger.error(e, exc_info = True)


###################################################
# Test code
###################################################
if __name__ == "__main__":
    run() 









