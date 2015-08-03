__author__ = 'admin'
import os
from subprocess import call,Popen
import subprocess
from multiprocessing import Process
import multiprocessing
import re
import traceback
try:
    import urllib.request as urllib2
except ImportError:
    import urllib2
import logging
from glob import glob
import json

from webmocker.mock_helper import pretender_defaults,MockRequest,MockResponse,HttpMock

LOGGER = logging.getLogger("webmocker")
not_supported_filters = ["doesNotMatch"]
pid = None
server_process = None

def start_pretend(port_number = pretender_defaults.portno):
    global server_process
    server_process = Process(name='pretend', args=(port_number,),target=pretend)
    server_process.start()

def pretend(port_number):
    global pid
    pid = Popen("python -m pretend_extended.server.server --host 0.0.0.0 --port "+ str(port_number), stdout=subprocess.PIPE, shell=True)

def stop_pretend():
    if(server_process != None):
        server_process.terminate()

def get_url_from_json(request_json):
    url = get_url(request_json)
    # handle query params
    if( 'queryParameters' not in request_json): return url
    query_param = format_query_string(request_json['queryParameters'])
    query_param = '('+ query_param + '&?){'+ str(len(request_json['queryParameters'])) +'}'
    url = url + ('\?' if query_param!='' else '') + query_param
    return url

def get_body_from_json(request_json):
    body = request_json['body'] if 'body' in request_json else pretender_defaults.request_body
    if( 'bodyPatterns' not in request_json):
        return body
    body = convert_list_to_dict(request_json['bodyPatterns'])
    body_str = ''
    if 'matches' in body:
        body_str = body_str + body['matches']
    if 'doesNotMatch' in body:
        body_str = body_str + 'PPP'+ body['doesNotMatch']
    return body_str

def get_headers_from_json(request_json):
    if('headers' not in request_json):
        return {}
    headers = convert_json_to_dict(request_json['headers'])
    return headers

def convert_json_to_dict(json_element):
    # delete_keys(json_element,not_supported_filters)
    return { header : get_header_value(value) for header,value in json_element.items()}

def delete_keys(json_element,keys_to_delete):
     remove = [header for header,value in json_element.items() if isinstance(value, dict) and key_in_list(value,keys_to_delete)]
     for k in remove: del json_element[k]


def convert_list_to_dict(dict_element):
    # return [key_value_pair for key_value_pair in dict_element  if isinstance(key_value_pair, dict) and key_in_list(key_value_pair,["matches","doesNotMatch"])]
    return dict([(key,d[key]) for d in dict_element for key in d])


def key_in_list(value,keys_to_delete):
    result = False
    for key in keys_to_delete:
        result = result or key in value
    return result

def get_header_value(value):
    if isinstance(value, dict):
        if('equalTo' in value): return re.escape(value['equalTo'])
        elif('matches' in value): return '.*?'+ value['matches'] +'.*'
        elif('contains' in value): return '.*?'+value['contains']+'.*'
        elif('doesNotMatch' in value): return 'PPP.*?'+value['doesNotMatch'] +'.*'
    return value

def format_query_string(query_params):
    query_param = ''
    for param,value in query_params.items():
        query_param = query_param + ('&?|' if query_param!='' else '') + get_param_value(param,value)
    return query_param

def get_param_value(param,value):
     if isinstance(value, dict):
        if('contains' in value):
           return  param +'=.*?'+ re.escape(urllib2.quote(value['contains'])).replace('\%','%')+'.*?'
        elif('equalto' in value):
            return param +'='+  re.escape(urllib2.quote(value['equalto'])).replace('\%','%')
        elif('matches' in value):
            return param +'='+  value['matches'].replace(' ','%20')
     else:
        return param +'='+ value.replace(' ','%20')

def get_response_headers_from_json(response_json):
    response_headers = {}
    if('headers' not in response_json):
        return response_headers
    for header,value in response_json['headers'].items():
       response_headers[header] = value
    return response_headers

def process_stubs(stubs):
    mock = HttpMock.Mock(pretender_defaults.portno,pretender_defaults.stub_name)       # create a HTTPMock Object
    for stub in stubs:                             # iterate for each stub in the json
        try:
            request = MockRequest.Request()
            response = MockResponse.Response()
            if ('request' in stub):
                request.set_request_entities(stub['request'])
            if ('response' in stub):
                response.set_response_entities(stub['response'])
            mock.mock_request(request,response)
        except:
            traceback.print_exc()

def process_stub_files(stub_files_path):
    for stub_file in glob(stub_files_path+'*.json'):   # iterate for each json file
        try:
            LOGGER.debug(stub_file)
            stubs = json.load(open(stub_file))
            LOGGER.debug(stub_file)
            process_stubs(stubs)
        except:
            LOGGER.debug('Exception while Processing Json file')


def get_url(request_json):
    url = request_json['url'].replace('?','\?')+'$' if 'url' in request_json else pretender_defaults.url
    url = request_json['urlPattern'].replace('?','\?') if 'urlPattern' in request_json else url
    return request_json['urlPath'].replace('?','\?')+'(/.*)?' if 'urlPath' in request_json else url

def get_response_body_from_json(response_body):
    if(os.path.exists(response_body)):
        file = open(response_body, 'r')
        file_content = file.read()
        return file_content
    else:
        return response_body
