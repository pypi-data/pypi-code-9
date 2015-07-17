#!/usr/bin/env python   

import requests
from bs4 import BeautifulSoup

from constants import BASE_URL

def get_result(usn):
    """
    Returns a html object for the requested usn
    """
    payload = {'rid':usn, 'submit':'SUBMIT'} 
    response = requests.get(BASE_URL, params=payload).text
    return BeautifulSoup(response, 'html.parser')

def get_reval_result(usn):
    """
    Returns a html object for the requested usn
    """
    payload = {'rid':usn, 'submit':'SUBMIT'} 
    response = requests.get(REVAL_URL, params=payload).text
    return html.fromstring(response)
