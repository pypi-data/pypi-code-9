from frasco import Feature, action, command, request, session, current_app, current_context, hook
import pygeoip
import os


COUNTRY_DB_URL = "http://geolite.maxmind.com/download/geoip/database/GeoLiteCountry/GeoIP.dat.gz"
CITY_DB_URL = "http://geolite.maxmind.com/download/geoip/database/GeoLiteCity.dat.gz"


class GeoipFeature(Feature):
    name = "geoip"
    defaults = {"country_db": "GeoIP.dat",
                "city_db": "GeoLiteCity.dat",
                "auto_geolocate": True}

    @hook()
    def before_request(self, *args, **kwargs):
        if self.options["auto_geolocate"]:
            self.geolocate_country()

    @action(default_option="addr", as_="geo_country_code")
    def geolocate_country(self, addr=None, use_session_cache=True):
        country = None
        if use_session_cache and "geo_country_code" in session:
            country = session["geo_country_code"]
        else:
            gi = pygeoip.GeoIP(self.options["country_db"])
            country = gi.country_code_by_addr(addr or self.get_remote_addr())
            if use_session_cache:
                session["geo_country_code"] = country
        current_context.data.geo_country_code = country
        return country

    @action(default_option="addr", as_="geo_city")
    def geolocate_city(self, addr=None, use_session_cache=True):
        city = None
        if use_session_cache and "geo_city" in session:
            city = session["geo_city"]
        else:
            gi = pygeoip.GeoIP(self.options["city_db"])
            city = gi.record_by_addr(addr or self.get_remote_addr())
            if use_session_cache:
                session["geo_city"] = city
        current_context.data.geo_city = city
        return city

    @action("clear_geo_cache")
    def clear_cache(self):
        session.pop("geo_country_code", None)
        session.pop("geo_city", None)

    def get_remote_addr(self):
        if current_app.debug and "__geoaddr" in request.values:
            return request.values["__geoaddr"]
        return request.remote_addr

    @command('dlcountries')
    def download_country_db(self):
        os.system("wget -O - %s | gunzip -c > %s" % (COUNTRY_DB_URL, self.options["country_db"]))

    @command('dlcities')
    def download_city_db(self):
        os.system("wget -O - %s | gunzip -c > %s" % (CITY_DB_URL, self.options["city_db"]))