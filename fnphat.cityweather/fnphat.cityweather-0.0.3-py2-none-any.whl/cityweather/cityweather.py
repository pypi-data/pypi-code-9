import data_gc_ca_api.cityweather as _ec

class CityWeather(object):
    TIMESTAMP = 'currentConditions/dateTime/timeStamp'
    HUMIDEX = 'currentConditions/humidex'
    TEMPERATURE = 'currentConditions/temperature'
    HUMIDITY = 'currentConditions/relativeHumidity'
    DEW_POINT = 'currentConditions/dewpoint'

    def __init__(self, city_name):
        self.city_name = city_name
        self.ec_city = None
    
    def update(self):
        index = _ec.CityIndex()
        if index.is_city(self.city_name):
            self.ec_city = _ec.City(index.data_url(self.city_name))
            return True
        else:
            return False
    
    def _get_metric(self, metric):
        if self.ec_city is not None:
            return self.ec_city.get_quantity(metric)
        else:
            return None
    
    def _get_attribute(self, path, attribute):
        if self.ec_city is not None:
            """Get the atribute of the element at XPath path"""
            element = self.ec_city.tree.find(path)
            if element is not None and element.attrib.has_key(attribute):
                return element.attrib[attribute]
            else: 
                return None
        else:
            return None

    def _get_metric_and_units(self, metric):
        return self._get_metric(metric), self._get_attribute(metric, 'units')

    def timestamp(self):
        return self._get_metric(self.TIMESTAMP)
        
    def temperature(self):
        return self._get_metric_and_units(self.TEMPERATURE)

    def humidity(self):
        return self._get_metric_and_units(self.HUMIDITY)

    def dew_point(self):
        return self._get_metric_and_units(self.DEW_POINT)
        
    def humidex(self):
        return self._get_metric_and_units(self.HUMIDEX)