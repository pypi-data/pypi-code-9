#!/usr/bin/env python
# module_template.py
"""
Run a search on Splunk, return job information
"""

from __future__ import print_function
import argparse
import sys
import re
import splunklib.client
import splunklib.results

def search_splunk(query, username, password):
    """Run a search on Splunk, return job information"""

    HOST = config.SPLUNK_HOST
    PORT = config.SPLUNK_PORT
    USERNAME = config.SPLUNK_USERNAME
    PASSWORD = config.SPLUNK_PASSWORD
    SCHEME = "https"

    service = splunklib.client.connect(
        host=HOST,
        port=PORT,
        username=USERNAME,
        password=PASSWORD,
        scheme=SCHEME)

    jobs = service.jobs

    # Run a blocking search--search everything, return 1st 100 events
    kwargs_blockingsearch = {'exec_mode': 'blocking'}
    # A blocking search returns the job's SID when the search is done
    job = jobs.create(query, **kwargs_blockingsearch)
    job.set_ttl(24*60*60) # set job time to live for 24 hours

    splunk_job_properties =  {
        'sid' : job['sid'],
        'num_events' : job['eventCount'],
        'num_results' : job['resultCount'],
        'job_link' : 'https://splunk-head03.ibechtel.com:8000/en-US/app/search/search?sid={}'.format(job['sid']),
        'query' : query
    }

    return splunk_job_properties

### WebAPI ###
from scrypture import webapi
class WebAPI(webapi.WebAPI):
    query = webapi.line_input('Query')
    username = webapi.line_input('Splunk Username')
    password = webapi.password_input('Splunk Password')
    submit_button = webapi.submit_button('Splunk!')

    def run(self, form_input):
        query = form_input['query']
        username = form_input['username']
        password = form_input['password']

        output = search_splunk(query, username, password)

        return {'output_type' : 'simple',
                'output' : output}
