#!/usr/bin/env python   

import requests
from bs4 import BeautifulSoup

from constants import BASE_URL

def get_result(usn):
    """
    Returns a html object for the requested usn
    """
    payload = {'rid':usn, 'submit':'SUBMIT'} 
    print "Hey, there!"
    print "Hold on!, till I get your result.."
    try:
    	response = requests.get(BASE_URL, params=payload).text
    	return BeautifulSoup(response, 'html.parser')
    except requests.exceptions.Timeout as e:
    	print "Sorry, Time Out : ", e 
    except requests.exceptions.TooManyRedirects as e:
    	print "Sorry, Too Many Redirects : ", e
    except requests.exceptions.RequestException as e:
    	print "Sorry, Catastrophic Error : ",e	

def get_entire_result(usn):
    """
    Returns a html object for the requested usn
    """
    payload = {'rid':usn, 'submit':'SUBMIT'} 
    try:
        response = requests.get(BASE_URL, params=payload).text
        return BeautifulSoup(response, 'html.parser')
    except requests.exceptions.Timeout as e:
        print "\nSorry, Time Out : ", e 
    except requests.exceptions.TooManyRedirects as e:
        print "\nSorry, Too Many Redirects : ", e
    except requests.exceptions.RequestException as e:
        print "\nSorry, Catastrophic Error : ", e  
