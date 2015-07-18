import logging
from falconer.data import daos


def setup_database():
    """
        Sets up the database connections.
    """
    daos.connect()



def setup_logging():
    """
        Sets up logging for the system.
    """
    logFormatter = logging.Formatter("%(asctime)s [%(threadName)-12.12s] [%(levelname)-5.5s]  %(message)s")
    rootLogger = logging.getLogger()

    #fileHandler = logging.FileHandler("{0}/{1}.log".format(logPath, fileName))
    #fileHandler.setFormatter(logFormatter)
    #rootLogger.addHandler(fileHandler)

    consoleHandler = logging.StreamHandler()
    consoleHandler.setFormatter(logFormatter)
    rootLogger.addHandler(consoleHandler)
