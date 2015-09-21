#!/usr/bin/python
import os
import smtplib
import logging
# sudo pip install GitPython
import git
import jinja2
from requests.auth import HTTPBasicAuth
import base64
import requests
import json
import sys
from novaclient import client

# TODO complete GPG file update
# TODO write all log, error info's to string buffer and print in once.
log = logging.getLogger(__name__)

_quota_resources = ['instances', 'cores', 'ram',
                    'floating_ips', 'fixed_ips', 'metadata_items',
                    'injected_files', 'injected_file_content_bytes',
                    'injected_file_path_bytes', 'key_pairs',
                    'security_groups', 'security_group_rules',
                    'server_groups', 'server_group_members']

def get_openstack_connections(region):
    OS_USERNAME = os.environ.get('OS_USERNAME_' + region,'')
    if ( is_blank_or_null(OS_USERNAME)):
        log.error("No environment variable found with the name OS_USERNAME_" + region)   
    OS_PASSWORD = os.environ.get('OS_PASSWORD_' + region,'')
    if ( is_blank_or_null(OS_PASSWORD)):
        log.error("No environment variable found with the name OS_PASSWORD_" + region)
    OS_TENANT_NAME = os.environ.get('OS_TENANT_NAME_'+ region,'')
    if ( is_blank_or_null(OS_TENANT_NAME)):
        log.error("No environment variable found with the name OS_TENANT_NAME_" + region)
    OS_AUTH_URL = os.environ.get('OS_AUTH_URL_' + region,'')
    if ( is_blank_or_null(OS_AUTH_URL)):
        log.error("No environment variable found with the name OS_AUTH_URL_"+ region)
    d = {}
    d['username'] = OS_USERNAME
    d['api_key'] = OS_PASSWORD
    d['auth_url'] = OS_AUTH_URL
    d['project_id'] = OS_TENANT_NAME
    #nova = client.Client(username=OS_USERNAME, password=OS_PASSWORD, tenant_name=OS_TENANT_NAME, auth_url=OS_AUTH_URL)
    nova = client.Client("2", **d)
    return nova

def is_blank_or_null(value):
    if ((value == '') or (len(value) == 0)):
        return True
    else:
        return False
    
def mainmethod(args):
    try:
        regions=args.regions.split(',')
        for region in regions: 
                       
            log.info("Configuring openstack connection in  "+region)
            updates = {}
            for resource in _quota_resources:
                val = getattr(args, resource, None)
                if val is not None:
                    updates[resource] = val

            if updates:
                log.info("connecting to open_stack")
                nova = get_openstack_connections(region)
                nova.quotas.update(args.tenant, **updates)
            
    except Exception, e:
        print e  
        
if __name__ == '__main__':
    
    mainmethod(args)        


