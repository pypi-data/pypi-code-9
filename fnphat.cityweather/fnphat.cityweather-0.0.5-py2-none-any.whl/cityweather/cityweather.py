import data_gc_ca_api.cityweather as _ec
import arrow as _arrow

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
        #timestamp format: 20150806130000 = 2015-08-06 13:00:00 UTC
        timestamp = self._get_metric(self.TIMESTAMP)
        if timestamp is not None:
            timestamp = _arrow.get(timestamp, 'YYYYMMDDHHmmss').to('local')
        return timestamp
        
    def temperature(self):
        temper, units = self._get_metric_and_units(self.TEMPERATURE)
        if temper is not None:
            temper = float(temper)
        return temper, units

    def humidity(self):
        humidity, units = self._get_metric_and_units(self.HUMIDITY)
        if humidity is not None:
            humidity = int(humidity)
        return humidity, units       

    def dew_point(self):
        dew_point, units = self._get_metric_and_units(self.DEW_POINT)
        if dew_point is not None:
            dew_point = float(dew_point)
        return dew_point, units        
        
    def humidex(self):
        humidex, units = self._get_metric_and_units(self.HUMIDEX)
        if humidex is not None:
            humidex = int(humidex)
        return humidex, units    

