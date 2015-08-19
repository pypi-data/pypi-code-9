# -*- coding: utf-8 -*-
"""
This file is part of Ludolph: Weather plugin
Copyright (C) 2015 Erigones, s. r. o.

See the LICENSE file for copying permission.
"""
import requests

from ludolph.command import command, CommandError
from .weather import WeatherLudolphPlugin


class OpenWeatherMap(WeatherLudolphPlugin):
    """
    Ludolph Weather plugin implementation using http://openweathermap.org.
    """
    api_base_url = 'http://api.openweathermap.org/data/2.5'
    api_url_current = api_base_url + '/weather?APPID={api_key}&q={location}&units=metric&type=accurate'
    api_url_forecast = api_base_url + '/forecast/daily?APPID={api_key}&q={location}&units=metric&cnt={days}' \
                                      '&type=accurate'
    headers = {
        'User-Agent': 'Ludolph/Weather/%s' % WeatherLudolphPlugin.__version__,
        'Accept': 'application/json; indent=4',
        'Content-Type': 'application/json; indent=4',
    }
    _subject = 'Weather for **{city},{country}**'
    _day_line = ('-------- {dt} -------- \n'
                 ' {desc} \n'
                 ' Temperature: {temp}°C ^^max: {temp_max}°C, min: {temp_min}°C^^ \n'
                 ' Humidity: {humidity} %, Pressure: {pressure} kPa \n'
                 ' Cloudiness: {clouds} %, Wind speed: {wind_speed} m/s, Wind direction: {wind_deg}° \n')

    def get_weather(self, location, days=0):
        api_key = self.config.get('api_key', None)
        assert api_key, 'api_key configuration is missing'

        if days > 0:
            api_url = self.api_url_forecast.format(api_key=api_key, location=location, days=days + 1)
        else:
            api_url = self.api_url_current.format(api_key=api_key, location=location)

        print(api_url)
        response = requests.get(api_url, headers=self.headers)

        if response.status_code != requests.codes.ok:
            raise CommandError(response)

        res = response.json()
        code = int(res['cod'])

        if code != requests.codes.ok:
            raise CommandError(res.get('message', res))

        return res

    # noinspection PyUnusedLocal
    @command
    def weather(self, msg, *args):
        """
        Show current weather information or weather forecast for one location.

        Usage: weather <city name,[country code]>
        Usage: weather <city name,[country code]> <now|tomorrow>
        Usage: weather <city name,[country code]> +<number of days of weather forecast (6 max)>
        """
        subject, day_line = self._subject, self._day_line
        location, days = self._parse_params(*args)
        data = self.get_weather(location, days=days)
        # TODO: +rain/snow information

        if days:
            res = [subject.format(city=data['city']['name'], country=data['city']['country']), '']

            for day_data in data.get('list', ()):
                temp = day_data.pop('temp')
                res.append(day_line.format(
                    dt=self._epoch_to_dt_str(day_data.pop('dt')),
                    desc=day_data['weather'][0]['description'].capitalize(),
                    temp=temp['day'],
                    temp_max=temp['max'],
                    temp_min=temp['min'],
                    wind_speed=day_data.get('speed'),
                    wind_deg=day_data.get('deg'),
                    **day_data  # humidity, pressure, clouds
                ))

        else:
            loc = data['sys']
            subject += ' ^^sunrise: {sunrise}, sunset: {sunset}^^'
            res = [
                subject.format(
                    city=data['name'],
                    country=loc['country'],
                    sunrise=self._epoch_to_dt_str(loc['sunrise']),
                    sunset=self._epoch_to_dt_str(loc['sunset']),
                ),
                '',
                day_line.format(
                    dt=self._epoch_to_dt_str(data['dt']),
                    desc=data['weather'][0]['description'].capitalize(),
                    clouds=data.get('clouds', {}).get('all'),
                    wind_speed=data.get('wind', {}).get('speed'),
                    wind_deg=data.get('wind', {}).get('deg'),
                    **data['main']  # temp, temp_max, temp_min, humidity, pressure
                )
            ]

        return '\n'.join(res)
