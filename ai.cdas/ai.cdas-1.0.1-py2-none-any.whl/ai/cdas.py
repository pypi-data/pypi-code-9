
import requests
import wget
import tempfile
import os
import numpy
from datetime import *

__BASEURL__ = 'http://cdaweb.gsfc.nasa.gov/WS/cdasr/1'
__HEADERS__ = {'accept': 'application/json'}

def get_dataviews():
    url = '/'.join([__BASEURL__, 'dataviews'])
    response = requests.get(url, headers=__HEADERS__)
    return response.json()

def get_observatory_groups(dataview, instrumentType=None):
    url = '/'.join([__BASEURL__, 'dataviews', dataview, 'observatoryGroups'])
    params = {'instrumentType': instrumentType}
    response = requests.get(url, params=params, headers=__HEADERS__)
    return response.json()

def get_instrument_types(dataview, observatory=None, observatoryGroup=None):
    url = '/'.join([__BASEURL__, 'dataviews', dataview, 'instrumentTypes'])
    params = {'observatory': observatory, 'observatoryGroup': observatoryGroup}
    response = requests.get(url, params=params, headers=__HEADERS__)
    return response.json()

def get_instruments(dataview, observatory=None):
    url = '/'.join([__BASEURL__, 'dataviews', dataview, 'instruments'])
    params = {'observatory': observatory}
    response = requests.get(url, params=params, headers=__HEADERS__)
    return response.json()

def get_observatories(dataview, instrument=None, instrumentType=None):
    url = '/'.join([__BASEURL__, 'dataviews', dataview, 'observatories'])
    params = {'instrument': instrument, 'instrumentType': instrumentType}
    response = requests.get(url, params=params, headers=__HEADERS__)
    return response.json()

def get_observatory_groups_and_instruments(dataview, instrumentType=None):
    url = '/'.join([__BASEURL__, 'dataviews', dataview, 'observatoryGroupsAndInstruments'])
    params = {'instrumentType': instrumentType}
    response = requests.get(url, params=params, headers=__HEADERS__)
    return response.json()

def get_datasets(dataview, observatoryGroup=None, instrumentType=None, 
    observatory=None, instrument=None, startDate=None, stopDate=None, 
    idPattern=None, labelPattern=None, notesPattern=None):
    url = '/'.join([__BASEURL__, 'dataviews', dataview, 'datasets'])
    params = {'observatoryGroup': observatoryGroup, 'instrumentType': instrumentType,
        'observatory': observatory, 'instrument': instrument,
        'startDate': startDate, 'stopDate': stopDate,
        'idPattern': idPattern, 'labelPattern': labelPattern, 'notesPattern': notesPattern}
    response = requests.get(url, params=params, headers=__HEADERS__)
    return response.json()

def get_inventory(dataview, dataset):
    url = '/'.join([__BASEURL__, 'dataviews', dataview, 'datasets', dataset, 'inventory'])
    response = requests.get(url, headers=__HEADERS__)
    return response.json()

def get_variables(dataview, dataset):
    url = '/'.join([__BASEURL__, 'dataviews', dataview, 'datasets', dataset, 'variables'])
    response = requests.get(url, headers=__HEADERS__)
    return response.json()

def get_data(dataview, dataset, startTime, stopTime, variables, cdf=False):
    url = '/'.join([__BASEURL__, 'dataviews', dataview, 'datasets', dataset, 'data', ','.join([startTime, stopTime]), ','.join(variables)])
    params = {}
    if cdf:
        params = {'format': 'cdf', 'cdfVersion': 3}
    else:
        params = {'format': 'text'}
    response = requests.get(url, params=params, headers=__HEADERS__)
    tmp_dir = tempfile.gettempdir()
    data_filename = wget.download(response.json()['FileDescription'][0]['Name'], tmp_dir)
    print ''
    data_path = os.path.join(tmp_dir, data_filename)
    if cdf:
        try:
            from spacepy import pycdf
            data = {k: numpy.array(v) for k, v in pycdf.CDF(data_path).copy().items()}
        except ImportError:
            print 'SpacePy and CDF are required for processing CDAS data in CDF format'
    else:
        try:
            from astropy.io import ascii
            rdr = ascii.get_reader(Reader=ascii.Basic)
            rdr.header.splitter.delimeter = ' '
            rdr.data.splitter.delimeter = ' '
            rdr.header.start_line = 0
            rdr.data.start_line = 0
            rdr.data.end_line = None
            rdr.header.comment = '#'
            rdr.data.comment = r'[^0-9]'
            rdr.data.splitter.process_line = lambda x: x.strip().replace(' ', '_', 1)
            table = rdr.read(data_path)
            data = dict()
            data[table.colnames[0]] = [datetime.strptime(x, '%d-%m-%Y_%H:%M:%S.%f') for x in table.columns[0]]
            for i in range(1, len(table.columns)):
                data[table.colnames[i]] = numpy.array(table.columns[i])
        except ImportError:
            print 'AstroPy is required for processing CDAS data in ASCII format'
    return data
