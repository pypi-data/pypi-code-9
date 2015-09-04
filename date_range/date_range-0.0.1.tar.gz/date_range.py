import datetime

def date_range(*args):
    '''
    range(stop) -> iterable of datetime.date objects
    range(start, stop[, step]) -> iterable of datetime.date objects

    >>> list(date_range(datetime.date(2015, 1, 1), datetime.date(2015, 1, 3)))
    [datetime.date(2015, 1, 1), datetime.date(2015, 1, 2)]

    >>> list(date_range(datetime.date(2015, 1, 1), datetime.date(2015, 1, 6), 2))
    [datetime.date(2015, 1, 1), datetime.date(2015, 1, 3), datetime.date(2015, 1, 5)]

    >>> list(date_range(datetime.date(2015, 1, 1), datetime.date(2015, 1, 6), datetime.timedelta(2)))
    [datetime.date(2015, 1, 1), datetime.date(2015, 1, 3), datetime.date(2015, 1, 5)]

    '''
    if len(args) == 3:
        start, stop, step = args
        if isinstance(step, datetime.timedelta):
            int_step = step.days
        else:
            int_step = step
        parsed_args = (start.toordinal(), stop.toordinal(), int_step)
    else:
        parsed_args = tuple(x.toordinal() for x in args)

    return map(datetime.date.fromordinal, range(*parsed_args))
