#!/usr/bin/env python
# -*- coding:utf-8 -*

from ma_classe import *
from my_logging import *

log = my_logging(console_level = DEBUG, logfile_level = INFO)
#log = my_logging()

logging.info('Test_pylogg\main.py démarre')


obj1 = ma_classe()
obj2 = ma_classe()

del obj1
obj2.plante_pas()

log.debug('Log avec logger')
logging.debug('Log avec logging')

obj2.plante()