import calendar


def anonymize(date, relative=False):
    """
    Returns a new date which is the middle of the given date's year, i.e.:
    * July 2, if the year is a leap year
    * July 1, otherwise
    
    Examples:
    
    >> from qiutil import dates
    >> dates.anonymize(datetime(year=2014, month=6, day=3)).strftime("%D")
    07/01/15
    >> # 2016 is a leap year.
    >> dates.anonymize(datetime(year=2016, month=1, day=12)).strftime("%D")
    07/02/16
    
    :param date: the input datetime
    :return: a new date which is the middle of the given date's year
    :rtype: datetime
    """
    day = 2 if calendar.isleap(date.year) else 1

    return date.replace(month=7, day=day)
