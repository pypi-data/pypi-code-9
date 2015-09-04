from . import Block
import re

class BlockWeather(Block):
    name = 'weather'
    validation = '(^|\+|-)[A-Z]{2,}$'
    known_elements = [
        ('RE', 'Recent'),
        ('MI', 'Shallow'),
        ('PR', 'Partial'),
        ('BC', 'Patches'),
        ('DR', 'Drifting'),
        ('BL', 'Blowing'),
        ('SH', 'Shower'),
        ('TS', 'Thunderstorm'),
        ('FZ', 'Freezing'),
        ('VC', 'in Vicinity 8-16km'),
        ('DZ', 'Drizzle'),
        ('RA', 'Rain'),
        ('SN', 'Snow'),
        ('SG', 'Snow Grains'),
        ('IC', 'Ice Crystals'),
        ('PL', 'Ice Pellets'),
        ('GS', 'Small Hails'),
        ('GR', 'Hail'),
        ('UP', 'Unidentified precipitation (autometar)'),
        ('BR', 'Mist, Humidity >= 80% 1000-1500m view'),
        ('HZ', 'Haze, Humidity < 80% <= 5000m view'),
        ('FG', 'Fog, < 1000m view'),
        ('FU', 'Smoke'),
        ('DU', 'Dust'),
        ('SA', 'Sand'),
        ('VA', 'Volcanic Ash'),
        ('SQ', 'Sqalls'),
        ('PO', 'Dust and Sand whirls'),
        ('FC', 'Funnel Cloud, Tornados'),
        ('DS', 'Duststorm'),
        ('SS', 'Sandstorm'),
        ('NSW', 'Nil Significant Weather'),
        ('FG', 'Fog Level 1, 0100-0900m view'),
        ('PRFG', 'Fog Level 2, 0500-1500m view'),
        ('BCFG', 'Fog Level 3, 1000-3000m view'),
        ('MIFG', 'Fog Level 4, 1000-5000m view')
    ]

    def _parse(self, regex, callback=None):
        #if not super(BlockWeather, self)._parse(regex, callback):
        #    return

        weathers = []
        for x in self.known_elements:
            if isinstance(x, (tuple,)):
                description = x[1]
                x = x[0]
            else:
                description = x

            if self.block[0] == '+':
                description = '%s %s' % ('Heavy', description)
            if self.block[0] == '-':
                description = '%s %s' % ('Light', description)

            if re.search(x, self.block):
                weathers.append(description)
        return [" ".join(weathers)]

    def validate(self):
        if not super(BlockWeather, self).validate():
            return

        for x in ['^TEMPO$', '^TAF$', '^BECMG$', 'FM']:
            if re.search(x, self.block, re.I | re.S | re.M):
                return

        for x in self.known_elements:
            if isinstance(x, (tuple,)):
                x = x[0]
            if re.search(x, self.block, re.I | re.S | re.M):
                return True
        return False

