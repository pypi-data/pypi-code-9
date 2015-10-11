# Low level utility functions used by the gaas cli cmds

import pprint
import sys
import os
import re
import requests
import json
# from gtrace import *


def error(code, msg):
    '''Pring the error msg and exit with code.'''
    print 'Error:', msg
    sys.exit(code)


__verbose = False
__slUsername = None
__slApiKey = None

def setVerbose(verbose):
    '''Set verbose to True or False.'''
    global __verbose
    __verbose = verbose

def verbose(msg):
    '''Print the msg if the verbose option was set.'''
    global __verbose
    if __verbose:  print msg


def getHeaders():
    '''Build the http header, specifically the sl username and api key Authorization.'''
    # return {'content-type': 'application/json', 'Authorization':'Basic '+os.environ['SLUSERNAME']+':'+os.environ['SLAPIKEY']}
    global __slUsername
    global __slApiKey
    return {'content-type': 'application/json', 'Authorization':'Basic '+__slUsername+':'+__slApiKey}


def getUrl(gaashost, uriPostfix):
    '''Convenience function to add the standard 1st part of the url for the rest calls.'''
    return gaashost + '/gaas/v1' + uriPostfix


def get(gaashost, uriPostfix, params=None, returnErrors=False):
    '''Run a GET REST API call and return the output. If returnsErrors=False and an error is returned by the rest call,
    this function will print the error msg and exit.'''
    r = requests.get(getUrl(gaashost, uriPostfix), headers=getHeaders(), params=params, verify=False)
    verbose('GET ' + r.url)
    if r.status_code != 200:
        if returnErrors:
            return {'error-code':r.status_code, 'error-msg':r.text}
        else:
            error(2, 'code='+str(r.status_code)+', GET '+r.url+', '+r.text)
    try:
        return unicode2string(r.json())
    except ValueError as e:
        # error(2, str(e)+', '+r.text)
        return r.text


def put(gaashost, uriPostfix, data=None, params=None):
    if data != None:
        j = json.dumps(data)
        # if testMode:
        #     print 'In test mode, pretending to run: PUT '+getUrl(gaashost, uriPostfix)+', data: '+j
        #     return ''
        # else:
        r = requests.put(getUrl(gaashost, uriPostfix), headers=getHeaders(), data=j, params=params, verify=False)
        verbose('PUT '+r.url+', data: '+j)
    else:
        # if testMode:
        #     print 'In test mode, pretending to run: PUT '+getUrl(gaashost, uriPostfix)
        #     return ''
        # else:
        r = requests.put(getUrl(gaashost, uriPostfix), headers=getHeaders(), params=params, verify=False)
        verbose('PUT '+r.url)
    if r.status_code != 201:
        error(2, 'code='+str(r.status_code)+', PUT '+r.url+', '+r.text)
    try:
        return unicode2string(r.json())
    except ValueError as e:
        error(2, str(e)+', '+r.text)


def post(gaashost, uriPostfix, data=None, params=None, files=None):
    if data != None:
        j = json.dumps(data)
        # if testMode and not doItEvenInTestMode:
        #     print 'In test mode, pretending to run: POST '+getUrl(gaashost, uriPostfix)+', data: '+j
        #     return ''
        # else:
        r = requests.post(getUrl(gaashost, uriPostfix), headers=getHeaders(), params=params, data=j, verify=False)
        verbose('POST '+r.url+', data: '+j)
    else:
        # if testMode and not doItEvenInTestMode:
        #     print 'In test mode, pretending to run: POST '+getUrl(gaashost, uriPostfix)
        #     return ''
        # else:
        r = requests.post(getUrl(gaashost, uriPostfix), headers=getHeaders(), params=params, verify=False)
        verbose('POST '+r.url)
    if r.status_code != 201:
        error(2, 'code='+str(r.status_code)+', POST '+r.url+', '+r.text)
    try:
        return unicode2string(r.json())
    except ValueError as e:
        error(2, str(e)+', '+r.text)


def unicode2string(inputVar):
    '''Convert all of the unicode strings in the specified variable (string, dict, list) to regular strings.'''
    if isinstance(inputVar, dict):
        return {unicode2string(key):unicode2string(value) for key,value in inputVar.iteritems()}
    elif isinstance(inputVar, list):
        return [unicode2string(element) for element in inputVar]
    elif isinstance(inputVar, unicode):
        return inputVar.encode('utf-8')
    else:
        return inputVar

def getSlCredentials():
    '''Look for the user's sl username and api key in environment variables and in their .softlayer file.
    If found, save them for this module to use (and return them to the caller), else exit with an error msg.'''
    global __slUsername
    global __slApiKey
    if 'SLUSERNAME' in os.environ:  __slUsername = os.environ['SLUSERNAME']
    if 'SLAPIKEY'  in os.environ:  __slApiKey = os.environ['SLAPIKEY']
    if __slUsername and __slApiKey:  return __slUsername, __slApiKey
    # check the .softlayer file
    username, apikey = readSlConfigFile()
    if not __slUsername:  __slUsername = username
    if not __slApiKey:  __slApiKey = apikey
    if not __slUsername or not __slApiKey:  error(2, 'Must specify your SoftLayer username and API key in environment variables or in your .softlayer file')
    # print __slUsername, __slApiKey
    return __slUsername, __slApiKey


def readSlConfigFile():
    '''Read the .softlayer file, if it exists, to get the sl user and api key.'''
    filename = os.path.expanduser("~")+'/.softlayer'
    if not os.path.exists(filename):  return None, None
    try:
        f = open(filename, 'r')
    except Exception as e:
        error(2, 'can not open '+filename+': '+str(e))      # this will exit

    # look for "username =" and "api_key ="
    userPattern = re.compile(r'^\s*username\s*=\s*(\S+)\s*$')
    apikeyPattern = re.compile(r'^\s*api_key\s*=\s*(\S+)\s*$')
    username = None
    apikey = None
    for line in f:
        match = userPattern.search(line)
        if match:
            username = match.group(1)
            continue
        match = apikeyPattern.search(line)
        if match:
            apikey = match.group(1)
            continue

    return username, apikey


def getGaasHost(args):
    '''Try to get the gaas svr host or ip from a variety of sources and return it.'''
    if args.gaashost:  return args.gaashost
    elif 'GAASHOST' in os.environ:  return os.environ['GAASHOST']
    else:  return 'https://108.168.254.196'         # this is gateway-as-a-service.com
