import logging

def init_logger(name, directory=".", log_level=logging.DEBUG):
    """Set up a logging system"""
    log = logging.getLogger(name)
    log.setLevel(logging.DEBUG)
    # The handler should only be set once for matching logger_names
    if not getattr(log, 'handler_set', None):
        formatter = logging.Formatter('%(asctime)s  %(levelname)s: '\
                                      '(%(module)s %(funcName)s) '
                                      '%(message)s', "%Y-%m-%dT%H:%M:%S")
        log_file = logging.FileHandler("{}/{}.log".format(directory,
                                                          name))
        log_file.setFormatter(formatter)
        log_file.setLevel(logging.DEBUG)
        log.addHandler(log_file)
        prt_screen = logging.StreamHandler()
        prt_screen.setLevel(logging.DEBUG)
        prt_screen.setFormatter(formatter)
        log.addHandler(prt_screen)
        log.handler_set = True
    return log
