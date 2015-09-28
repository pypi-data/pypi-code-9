from . import Receiver


class TafReceiver(Receiver):
    _url = 'http://weather.noaa.gov/pub/data/forecasts/taf/stations/%s.TXT'

    def receive(self):
        x = super(TafReceiver, self).receive()
        if x:
            return [' '.join(x)]
        return []

