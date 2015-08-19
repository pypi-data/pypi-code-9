# -*- coding: utf-8 -*-
"""
This file is part of Ludolph: Weather plugin
Copyright (C) 2015 Erigones, s. r. o.

See the LICENSE file for copying permission.
"""
from datetime import datetime
from pytz import timezone, UTC

from ludolph_weather import __version__
from ludolph.command import MissingParameter, CommandError
from ludolph.plugins.plugin import LudolphPlugin


class WeatherLudolphPlugin(LudolphPlugin):
    """
    Ludolph: Weather base class.

    Do not use directly. Subclass it and implement the missing methods + the weather command.
    """
    __version__ = __version__
    datetime_format = '%c'

    def __post_init__(self):
        self.timezone = timezone(self.config.get('timezone'))

    def _parse_params(self, *args):
        """Parse weather command parameters"""
        days = 0
        location = None

        if args:
            last_param = args[-1]
            location_end_idx = -1

            if last_param == 'now':
                days = 0
            elif last_param == 'tomorrow':
                days = 1
            elif last_param.startswith('+'):
                try:
                    days = int(last_param[1:])
                except ValueError:
                    raise CommandError('Invalid days parameter')
            else:
                location_end_idx = None

            location = ' '.join(args[:location_end_idx])

        if not location:
            location = self.config.get('default_location', None)

            if not location:
                raise MissingParameter

        return location, days

    @staticmethod
    def _epoch_to_dt(epoch):
        """Convert unix time to datetime object"""
        return datetime.utcfromtimestamp(epoch).replace(tzinfo=UTC)

    def _epoch_to_dt_str(self, epoch):
        """Convert unix time to datetime string adjusted by timezone information from config file"""
        dt = self._epoch_to_dt(epoch).astimezone(self.timezone)
        return dt.strftime(self.datetime_format)
