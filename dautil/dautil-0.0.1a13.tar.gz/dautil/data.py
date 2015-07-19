import pandas as pd
import numpy as np
from io import BytesIO
import zipfile
import gzip
from appdirs import AppDirs
import os
from pkg_resources import resource_filename
import urllib.request as urlrequest
from dautil import log_api


def download(url, out):
    response = urlrequest.urlopen(url)

    with open(out, 'wb') as f:
        f.write(response.read())
        log_api.conf_logger(__name__).warning('Downloaded ' + f.name)


def process_gzip(url, file_path):
    response = urlrequest.urlopen(url)
    compressed = BytesIO(response.read())
    decompressed = gzip.GzipFile(fileobj=compressed)

    with open(file_path, 'wb') as outfile:
        outfile.write(decompressed.read())


def process_zip(url, path, fname):
    response = urlrequest.urlopen(url)

    zip = zipfile.ZipFile(BytesIO(response.read()))

    return zip.extract(fname, path)


def get_data_dir():
    dirs = AppDirs("PythonDataAnalysisCookbook", "Ivan Idris")
    path = dirs.user_data_dir
    log_api.conf_logger(__name__).warning('Data dir ' + path)

    if not os.path.exists(path):
        os.mkdir(path)

    return path


class SPANFB():
    def __init__(self):
        self.fname = os.path.join(get_data_dir(),
                                  'facebook_combined.txt')

    def load(self):
        if not os.path.exists(self.fname):
            process_gzip('https://snap.stanford.edu/data/facebook_combined.txt.gz', self.fname)

        return self.fname


class Weather():
    @staticmethod
    def load():
        pckl = resource_filename(__name__, 'weather.pckl')
        return pd.read_pickle(pckl)

    @staticmethod
    def get_header(alias):
        mapping = {'WIND_DIR': 'Wind Dir',
                   'WIND_SPEED': 'W Speed, m/s',
                   'TEMP': 'Temp, °C',
                   'RAIN': 'Rain, mm',
                   'PRESSURE': 'Pres, hPa'}

        return mapping.get(alias, 'UNKNOWN')

    @staticmethod
    def fetch_DeBilt_weather():
        url = 'http://www.knmi.nl/klimatologie/daggegevens/datafiles3/260/etmgeg_260.zip'
        path = get_data_dir()
        file = process_zip(url, path, 'etmgeg_260.txt')
        df = pd.read_csv(file,
                         skiprows=47,
                         usecols=['YYYYMMDD', 'DDVEC', '   FG', '   TG', '   RH', '   PG'],             index_col=0, parse_dates=True, na_values='     ')

        df.columns = ['WIND_DIR', 'WIND_SPEED', 'TEMP', 'RAIN', 'PRESSURE']
        df[df['RAIN'] == -1] = 0.05/2
        df['WIND_SPEED'] = 0.1 * df['WIND_SPEED']
        df['TEMP'] = 0.1 * df['TEMP']
        df['RAIN'] = 0.1 * df['RAIN']
        df[df['PRESSURE'] < 1] = np.nan
        df['PRESSURE'] = 0.1 * df['PRESSURE']
        log_api.conf_logger(__name__).warning(df.index[-1])

        pckl = os.path.join(path, 'weather.pckl')
        df.to_pickle(pckl)
        assert df.equals(pd.read_pickle(pckl))
