from . import BasicPresenter


class HumanPresenter(BasicPresenter):
    def present(self):
        def _parse(key, data):
            method = '_parse_%s' % key
            if method in dir(self):
                return getattr(self, method)(data)
            return None

        data = []
        for airport in self._data:
            data.append(self._airport(airport['airport']))
            data.append('METAR')
            for key, value in airport['reports'][0].iteritems():
                x = _parse(key, value)
                if x:
                    data.append(x)
            data.append("\n")
            for taf_line in airport['reports'][1]:
                for taf_key in taf_line.iterkeys():
                    data.append(taf_key)
                    if not isinstance(taf_line[taf_key], (dict,)):
                        continue
                    for key, value in taf_line[taf_key].iteritems():
                        x = _parse(key, value)
                        if x:
                            data.append(x)
            data.append('TAF')
            data.append("\n")
        #return json.dumps(self._data, sort_keys=True, indent=4, separators=(',', ': '))
        return "\n".join(data)

    def _airport(self, data):
        return "Airport %s in %s at %s / %s" % (data['icao'], data['country'], data['latitude'], data['longitude'])

    def _parse_temperature(self, data):
        x = []
        if 'temperature' in data:
            x.append(u"Current Temperature %d degree. Dewpoint at %d and spread of %d degree." % (
                data['temperature']['temperature'],
                data['temperature']['dewpoint'],
                data['temperature']['spread']
            ))
        if 'temperature_forcast' in data:
            for t in data['temperature_forcast']:
                x.append("Forcast %s temperature of %d degree at %s" % (t['type'], t['temperature'], t['time']))
        return "\n".join(x)