import re
from block import Block
from blockpressure import BlockPressure
from blocktemperature import BlockTemperature
from blockview import BlockView
from blockwind import BlockWind
from blocktime import BlockTime
from blocktrend import BlockTrend
from blockweather import BlockWeather
from blockcloud import BlockCloud
from blockrunway import BlockRunway
from blockrunwayview import BlockRunwayView
from blockforcast import BlockForcast


class BlockFactory(object):
    parser = [BlockWind, BlockView, BlockTemperature, BlockPressure, BlockTime, BlockTrend, BlockWeather, BlockCloud, BlockRunway, BlockRunwayView, BlockForcast]
    elements = None

    def __init__(self, element_str):
        self.elements = element_str.split(' ')
        self.elements = filter(lambda y: True if len(y) > 0 else False, self.elements)

    def parse(self):
        if self.elements[0] == 'TAF':
            return self._parse_taf()
        return self._parse_metar()

    def _parse_taf(self):
        x = re.findall(r'((TEMPO|BECMG|FM|^TAF)(.*?))(?=\sTEMP|\sBECMG|\sFM|$)', ' '.join(self.elements))
        data = []
        for y in x:
            self.elements = str(y[0]).split(' ')
            data.append({str(y[1]): self._parse_metar(), '_raw': y[0]})
        return data

    def _parse_metar(self):
        data = {}
        for e in self.elements:
            for p in self.parser:
                x = p(e)
                if x.validate():
                    new_data = x.parse()
                    if x.name in data:
                        for (key, value) in new_data.iteritems():
                            if key in data[x.name]:
                                if isinstance(data[x.name][key], (list,)) and isinstance(value, (list,)):
                                    new_data[key] = new_data[key] + data[x.name][key] # merge lists
                                elif isinstance(data[x.name][key], (list,)) and not isinstance(value, (list,)):
                                    new_data[key] = data[x.name][key] + [new_data[key]] # append to list
                                else:
                                    new_data[key] = [new_data[key], data[x.name][key]] # create new list

                        data[x.name] = dict(data[x.name].items() + new_data.items())
                    else:
                        data[x.name] = new_data
                continue
        return data