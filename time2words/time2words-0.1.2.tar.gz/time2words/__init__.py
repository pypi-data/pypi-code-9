from num2words import num2words
from utils import _to_abs_seconds, _is_within_interval, _append_unit_suffix
from utils import _normalize
from chain import _Chain
from commands import _LessThan1M, _LessThan1H, _LessThan23H, _LessThan6D1H
from commands import _LessThan25D10H, _LessThan11MM, _LessThan10Y, _MoreThan10Y
from localization import locales, _default


def relative_time_to_text(l10n=locales.get(_default), **kwargs):
    """
    Return an aproximate textual representation of the provioded duration of
    time.

    Examples:
    relative_time_to_text(hours=6, minutes=34) -> "six and a half hours"
    relative_time_to_text(years=5, months=8, days=5) -> "less than six years"

    Keyword arguments:
    l10n -- The locale of the language for the result. Default is en_US.
    seconds
    minutes
    hours
    days
    weeks
    months
    years
    """
    kwargs = _normalize(**kwargs)

    cor = _Chain()
    cor.add(_LessThan1M(l10n, **kwargs))
    cor.add(_LessThan1H(l10n, **kwargs))
    cor.add(_LessThan23H(l10n, **kwargs))
    cor.add(_LessThan6D1H(l10n, **kwargs))
    cor.add(_LessThan25D10H(l10n, **kwargs))
    cor.add(_LessThan11MM(l10n, **kwargs))
    cor.add(_LessThan10Y(l10n, **kwargs))
    cor.add(_MoreThan10Y(l10n, **kwargs))
    return cor.run()

# TO DO: time_of_day_to_text
