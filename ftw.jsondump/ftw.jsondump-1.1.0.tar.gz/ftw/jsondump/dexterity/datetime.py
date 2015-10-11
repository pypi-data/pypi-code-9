from ftw.jsondump.dexterity.base import PlainFieldExtractor


class DatetimeExtrator(PlainFieldExtractor):

    def convert(self, value):
        if not value:
            return value

        return value.isoformat()


class TimedeltaExtractor(PlainFieldExtractor):

    def convert(self, value):
        if not value:
            return value

        return value.total_seconds()
