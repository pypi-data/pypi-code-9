#!/usr/bin/env python   

import requests
from lxml import html

from constants import BASE_URL

def get_result(usn):
    """
    Returns a html object for the requested usn
    """
    payload = {'rid':usn, 'submit':'SUBMIT'} 
    response = requests.get(BASE_URL, params=payload).text
    return html.fromstring(response)
