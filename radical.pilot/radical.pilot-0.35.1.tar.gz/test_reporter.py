#!/usr/bin/env python

import radical.utils as ru
import time


r = ru.Reporter (title='test\n')

r.header ('header\n')
r.info   ('info\t')
r.ok     ('ok\n')
r.info   ('info\t')
r.warn   ('warn\n')
r.info   ('info\t')
r.error  ('error\n')

r.info   ('info ?'); time.sleep(0.1)
r.ok     ('\bok\n')
r.info   ('info ?'); time.sleep(0.1)
r.warn   ('\bwarn\n')
r.info   ('info ?'); time.sleep(0.1)
r.error  ('\berr\n')

# time.sleep(1)

# r.set_style ('error', color='blue', style='ELTMLE', segment='X')
# r.error  ('error\n')

# r.set_style ('error', color='bold blue', style='ELMLE', segment='<')
# r.error  ('error\n')

log = ru.get_logger('demo')
log.demo('title', 'demo\n')
log.critical('crit')
log.error('err')
log.warn('warn')
log.info('info')
log.debug('debug')

log.demo('info', 'info')
log.demo('ok', '\\ok\n')

log.demo('info', 'info\nerrorerror')
log.demo('error', '\\err\n')
