import collectd

import collectdwriter


collectd.register_config(collectdwriter.config)
collectd.register_write(collectdwriter.write)
