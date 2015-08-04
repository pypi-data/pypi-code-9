from sys import stdout
import time


def asctime(t=None):
    """
    Converts the 8-tuple which contains:
    (year, month, mday, hour, minute, second, weekday, yearday)
    into a string in the form:
    'Sun Sep 16 01:03:52 1973\n'
    """

    t = list(t or time.lcaltime())
    month_name = [
        "Jan", "Feb", "Mar", "Apr", "May", "Jun",
        "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"
    ]

    day_name = [
        "Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"
    ]

    t[1] = month_name[t[1]]
    t[6] = day_name[t[6]]
    result = "{6} {1} {2:02} {3:02}:{4:02}:{5:02} {0}\n".format(*t)
    return result


class Logging(object):
    entry_format = "{time} : {pfx} : {log_lvl} : {msg}\n"

    prefix = 'OBDLIB'

    __logging_levels = (
        'CRITICAL',  # 0
        'ERROR',  # 1
        'WARNING',  # 2
        'INFO',  # 3
        'DEBUG',  # 4
        'NOTSET',  # 5,-1
    )

    def __logtime(self, t=None):
        """
        Converts the 8-tuple which contains:
        (year, month, mday, hour, minute, second, weekday, yearday)
        into a string in the form:
        '1981-05-31 01:03:59'
        """

        t = t or time.localtime()
        result = "{0:04}-{1:02}-{2:02} {3:02}:{4:02}:{5:02}".format(*t)
        return result

    def get_log_level(self, log_level):
        if log_level > len(self.__logging_levels) - 1:
            log_level = -1
        return self.__logging_levels[log_level]

    def __init__(self, log_level=1, duplicate_in_stdout=False, output=None):
        self.use_stdout = duplicate_in_stdout
        self.output_stream = output
        self.log_level = log_level

    def __call__(self, msg, level=5, force=False):
        if level > self.log_level:
            return
        out_msg = self.msg_format(msg, level)

        self.save_msg(self.output_stream, out_msg)

        if self.use_stdout or force:
            stdout.write(out_msg)

    def save_msg(self, stream, msg):
        if self.output_stream:
            # saves logging message
            with open(self.output_stream, 'wb') as stream:
                stream.write(msg)

    def msg_format(self, msg, level):
        return self.entry_format.format(time=self.__logtime(),
                                        pfx=self.prefix,
                                        log_lvl=self.get_log_level(level),
                                        msg=str(msg))

    def critical(self, msg):
        return self(msg, 0)

    def error(self, msg):
        return self(msg, 1)

    def warning(self, msg):
        return self(msg, 2)

    def info(self, msg):
        return self(msg, 3)

    def debug(self, msg):
        return self(msg, 4)

    def log(self, msg):
        return self(msg, 5)


logger = Logging(log_level=2)
