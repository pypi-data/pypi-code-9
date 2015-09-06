import os
import sys
import json

from absinthe import dirs
from absinthe.tools.logger import get_logger
from absinthe.tools.config import Config
from absinthe.absinthe_server import AbsintheServer

config_data = {}
with open(dirs.config_file) as f:
    config_data = json.load(f)

# init logger
logger = get_logger(config_data['logger'], 'server')
logger.info("Welcome to the lofasz. (pid: %d)" % os.getpid())

# init config
try:
    config = Config(logger)
    config.load(config_data['server'])
    logger.info('Config has been successfully loaded')
except Exception as e:
    logger.error('Exception occured during config parsing: ' + str(e))
    sys.exit(1)

server = AbsintheServer(config, logger)
server.start_command_server()
