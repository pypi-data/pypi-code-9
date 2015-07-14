from num2words import num2words
from chain import _Command


def _append_unit_suffix(value, suffix_singular, suffix_plural, presuffix=None):
    suffixed_value = []
    suffixed_value.append(num2words(value))
    if presuffix:
        suffixed_value.append(presuffix)
    suffixed_value.append(suffix_singular if value == 1 else suffix_plural)
    return " ".join(suffixed_value)


def _years_to_seconds(years):
    return years * 365 * 24 * 60 * 60


def _months_to_seconds(months):
    return months * (365/12) * 24 * 60 * 60


def _weeks_to_seconds(weeks):
    return weeks * 7 * 24 * 60 * 60


def _days_to_seconds(days):
    return days * 24 * 60 * 60


def _hours_to_seconds(hours):
    return hours * 60 * 60


def _minutes_to_seconds(minutes):
    return minutes * 60


def _to_abs_seconds(**kwargs):
    seconds = 0
    for key, value in kwargs.items():
        if key == "years":
            seconds = seconds + _years_to_seconds(value)
        if key == "months":
            seconds = seconds + _months_to_seconds(value)
        if key == "weeks":
            seconds = seconds + _weeks_to_seconds(value)
        if key == "days":
            seconds = seconds + _days_to_seconds(value)
        if key == "hours":
            seconds = seconds + _hours_to_seconds(value)
        if key == "minutes":
            seconds = seconds + _minutes_to_seconds(value)
        if key == "seconds":
            seconds = seconds + value
    return seconds


def _normalize(**kwargs):
    seconds = _to_abs_seconds(**kwargs)

    years = seconds / 31556900
    seconds = seconds % 31556900

    months = seconds / 2630000
    seconds = seconds % 2630000

    weeks = seconds / 604800
    seconds = seconds % 604800

    days = seconds / 86400
    seconds = seconds % 86400

    hours = seconds / 3600
    seconds = seconds % 3600

    minutes = seconds / 60
    seconds = seconds % 60

    return {
        'seconds': seconds,
        'minutes': minutes,
        'hours': hours,
        'days': days,
        'weeks': weeks,
        'months': months,
        'years': years
    }


def _is_within_interval(value, interval_start, interval_end):
    if value > interval_start and value <= interval_end:
        return True
    return False
