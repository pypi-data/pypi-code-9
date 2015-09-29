# encoding=utf-8
__author__ = 'LoveLYJ'
import pandas as pd
from numpy import loadtxt

def load_data_as_dataFrame(path, sep=','):
    return pd.read_table(path, sep, header = None)