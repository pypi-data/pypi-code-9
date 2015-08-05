from functions import *

from logger import log

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

	try:
		ListConfigFile = detect_all_config_file()
		LogFormat = get_all_log_formats(ListConfigFile)
		LogPattern = convert_all_format_to_regex(LogFormat)
		LogAccess = get_all_access_logs(ListConfigFile)
		machine_id = get_server_ip()

		#####################################
		log.debug("====== List Config File ======")
		log.debug(printList(ListConfigFile))

		log.debug("====== List Log Pattern ======")
		log.debug(printDict(LogPattern))

		log.debug("====== List Log Accesss ======")
		log.debug(printList(LogAccess))

		log.debug("====== Server IP  ======")
		log.debug(machine_id)
		####################################
		
		return (machine_id, LogAccess, LogPattern, ListConfigFile)
	except Exception, e:
		log.error(e, exc_info = True)


###################################################
# Test code
###################################################
if __name__ == "__main__":
	run()










