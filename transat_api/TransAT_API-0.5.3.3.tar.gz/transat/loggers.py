import logging
import os

def setup():
    FOLDER = 'logs'
    if not os.path.exists(FOLDER):
        os.makedirs(FOLDER)

    DEFAULT_LOG_FILE = 'default_transat_api.log'
    DEFAULT_LOG_FILE = os.path.join(FOLDER, DEFAULT_LOG_FILE)
    if os.path.exists(DEFAULT_LOG_FILE):
        os.remove(DEFAULT_LOG_FILE)

    LOG_FILE = 'transat_api.log'
    LOG_FILE = os.path.join(FOLDER, LOG_FILE)
    if os.path.exists(LOG_FILE):
        os.remove(LOG_FILE)

    FORMAT_STR = '%(asctime)s %(levelname)s %(name)s  %(message)s'


    formatter = logging.Formatter(FORMAT_STR)
    logging.basicConfig(format=FORMAT_STR,
                        filename=DEFAULT_LOG_FILE, level=logging.DEBUG, filemode='w')

    module_names = ['transat.simulation', 'transat.worker.worker', 'transat.software.installation', 'transat.setup.cad']
    for name in module_names:
      logger = logging.getLogger(name)
      hdlr_1 = logging.FileHandler(LOG_FILE)
      hdlr_1.setFormatter(formatter)
      logger.addHandler(hdlr_1)


