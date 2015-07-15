from chain import _Command
from utils import _to_abs_seconds, _append_unit_suffix


class _TimeCommand(_Command):

    def __init__(self, loc, **kwargs):
        super(_TimeCommand, self).__init__(**kwargs)
        self.loc = loc
        self.abs_seconds = _to_abs_seconds(**kwargs)


class _LessThan1M(_TimeCommand):

    def callback(self):
        # Less than a minute
        if self.abs_seconds >= _to_abs_seconds(minutes=1):
            return None

        time_in_words = []
        seconds = self.kwargs.get('seconds')
        time_in_words.append(_append_unit_suffix(seconds,
                                                 self.loc.second_singular,
                                                 self.loc.second_plural))
        return " ".join(time_in_words)


class _LessThan1H(_TimeCommand):

    def callback(self):
        # Between 1 minute and one hour
        if self.abs_seconds >= _to_abs_seconds(hours=1):
            return None

        time_in_words = []
        minutes = self.kwargs['minutes']
        time_in_words.append(self.loc.about)
        time_in_words.append(_append_unit_suffix(minutes,
                                                 self.loc.minute_singular,
                                                 self.loc.minute_plural))
        return " ".join(time_in_words)


class _LessThan23H(_TimeCommand):

    def callback(self):
        # Between 1 hour and 23 hours
        if self.abs_seconds >= _to_abs_seconds(hours=23):
            return None

        time_in_words = []
        hours = self.kwargs.get('hours')
        minutes = self.kwargs.get('minutes')
        if minutes <= 5:
            time_in_words.append(self.loc.about)
            time_in_words.append(_append_unit_suffix(hours,
                                                     self.loc.hour_singular,
                                                     self.loc.hour_plural))

        elif minutes < 25:
            time_in_words.append(self.loc.more_than)
            time_in_words.append(_append_unit_suffix(hours,
                                                     self.loc.hour_singular,
                                                     self.loc.hour_plural))

        elif minutes <= 35:
            time_in_words.append(_append_unit_suffix(hours,
                                                     self.loc.hour_singular,
                                                     self.loc.hour_plural,
                                                     self.loc.half))
        elif minutes < 55:
            time_in_words.append(self.loc.less_than)
            time_in_words.append(_append_unit_suffix(hours + 1,
                                                     self.loc.hour_singular,
                                                     self.loc.hour_plural))

        else:
            time_in_words.append(self.loc.about)
            time_in_words.append(_append_unit_suffix(hours + 1,
                                                     self.loc.hour_singular,
                                                     self.loc.hour_plural))

        return " ".join(time_in_words)


class _LessThan6D1H(_TimeCommand):

    def callback(self):
        if self.abs_seconds >= _to_abs_seconds(days=6, hours=1):
            return None
        time_in_words = []
        days = self.kwargs.get('days')
        hours = self.kwargs.get('hours')
        minutes = self.kwargs.get('minutes')

        if hours < 1:
            time_in_words.append(_append_unit_suffix(days,
                                                     self.loc.day_singular,
                                                     self.loc.day_plural))
        elif hours < 10:
            time_in_words.append(self.loc.a_little_more_than)
            time_in_words.append(
                _append_unit_suffix(days,
                                    self.loc.day_singular,
                                    self.loc.day_plural))
        elif hours < 14:
            time_in_words.append(self.loc.about)
            time_in_words.append(
                _append_unit_suffix(days,
                                    self.loc.day_singular,
                                    self.loc.day_plural,
                                    self.loc.half))
        elif hours < 23:
            time_in_words.append(self.loc.a_little_less_than)
            time_in_words.append(
                _append_unit_suffix(days + 1,
                                    self.loc.day_singular,
                                    self.loc.day_plural))
        else:
            time_in_words.append(_append_unit_suffix(days + 1,
                                                     self.loc.day_singular,
                                                     self.loc.day_plural))

        return " ".join(time_in_words)


class _LessThan25D10H(_TimeCommand):

    def callback(self):
        if self.abs_seconds >= _to_abs_seconds(days=25, hours=10):
            return None
        time_in_words = []
        weeks = self.kwargs.get('weeks')
        days = self.kwargs.get('days')

        if days < 2:
            time_in_words.append(self.loc.about)
            time_in_words.append(
                _append_unit_suffix(weeks, self.loc.week_singular,
                                    self.loc.week_plural))
        elif days < 5:
            time_in_words.append(self.loc.about)
            time_in_words.append(
                _append_unit_suffix(weeks, self.loc.week_singular,
                                    self.loc.week_plural, self.loc.half))
        else:
            time_in_words.append(self.loc.about)
            time_in_words.append(
                _append_unit_suffix(weeks + 1, self.loc.week_singular,
                                    self.loc.week_plural))

        return " ".join(time_in_words)


class _LessThan11MM(_TimeCommand):

    def callback(self):
        if self.abs_seconds >= _to_abs_seconds(months=11):
            return None

        time_in_words = []
        months = self.kwargs.get('months')
        weeks = self.kwargs.get('weeks')
        days = self.kwargs.get('days')

        if weeks < 1:
            time_in_words.append(self.loc.about)
            time_in_words.append(
                _append_unit_suffix(months, self.loc.month_singular,
                                    self.loc.month_plural))

        elif _to_abs_seconds(weeks=weeks, days=days) <\
                _to_abs_seconds(months=1) - _to_abs_seconds(weeks=1):
            time_in_words.append(self.loc.about)
            time_in_words.append(
                _append_unit_suffix(months, self.loc.month_singular,
                                    self.loc.month_plural, self.loc.half))
        else:
            time_in_words.append(self.loc.about)
            time_in_words.append(
                _append_unit_suffix(months + 1, self.loc.month_singular,
                                    self.loc.month_plural))
        return " ".join(time_in_words)


class _LessThan10Y(_TimeCommand):

    def callback(self):
        if self.abs_seconds >= _to_abs_seconds(years=10):
            return None
        time_in_words = []
        years = self.kwargs.get('years')
        months = self.kwargs.get('months')

        if months < 1:
            time_in_words.append(self.loc.about)
            time_in_words.append(
                _append_unit_suffix(years, self.loc.year_singular,
                                    self.loc.year_plural))
        elif months < 4:
            time_in_words.append(self.loc.more_than)
            time_in_words.append(
                _append_unit_suffix(years, self.loc.year_singular,
                                    self.loc.year_plural))
        elif months < 8:
            time_in_words.append(self.loc.about)
            time_in_words.append(
                _append_unit_suffix(years, self.loc.year_singular,
                                    self.loc.year_plural, self.loc.half))
        elif months < 11:
            time_in_words.append(self.loc.less_than)
            time_in_words.append(
                _append_unit_suffix(years + 1, self.loc.year_singular,
                                    self.loc.year_plural))
        else:
            time_in_words.append(self.loc.about)
            time_in_words.append(
                _append_unit_suffix(years + 1, self.loc.year_singular,
                                    self.loc.year_plural))

        return " ".join(time_in_words)


class _MoreThan10Y(_TimeCommand):

    def callback(self):
        time_in_words = []
        years = self.kwargs.get('years')
        months = self.kwargs.get('months')

        if months < 6:
            time_in_words.append(self.loc.about)
            time_in_words.append(
                _append_unit_suffix(years, self.loc.year_singular,
                                    self.loc.year_plural))
        else:
            time_in_words.append(self.loc.about)
            time_in_words.append(
                _append_unit_suffix(years + 1, self.loc.year_singular,
                                    self.loc.year_plural))

        return " ".join(time_in_words)
