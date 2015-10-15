#! /usr/bin/python
# __author__ = 'sadaqatullah'

"""
This is a plugin that works between ElasticSearch and Nagios. This Plugin takes status report
from ElasticSearch and puts it into Nagios for Nagios to understand. This plugin is specifically
for Gunicorn working with statsd. Statsd Takes data from Gunicorn and posts it into ElasticSearch.
Then this plugin takes required data from the elasticsearch and transforms it for nagios. It tells
Nagios maximum number of workers working in Gunicorn, Request Rate that Gunicorn is facing, Average
Request Duration that Gunicorn is taking.
"""

import argparse
import nagiosplugin
import time
import datetime
from elasticsearch import Elasticsearch


class Gunicorn_Data_Fetch(object):
    """
     This Class is used to fetch data from elastic search using Aggregation Average Query
     The current data is from 28th of September. But will be updated soon

     Update: 2015/10/01:
        Data is taken from the current Date Such that the Data this project takes is
     of "datetime.datetime.today()". This is helpful in automated daily update of
     data in ElasticSearch.

     Update: 2015/10/07:
        Gunicorn Data is shown on the Nagios with three different Services. Plugin works on
     ranges to be for warning and critical that need to be passed in as arguments. Plugin also
     takes the type of report user wants such as requestduration, requestrate, or workers. Plugin
     requires users to give time frame to take data from in minutes.

     Update: 2015/10/08:
        Code is Logically improved and more clean. Along with some minute error handling.
    """
    __es__ = Elasticsearch()

    def __init__(self, timechecker, indexerstring):

        self.timechecker = timechecker
        # self.indexerstring = "stats-2015.10.07"
        self.indexerstring = indexerstring

    def get_gunicorn_workers(self):
        """
        This function returns Maxworkers from ElasticSearch
        """
        # elasticresult = self.__es__.search(index="stats-2015.10.07", body={
        elasticresult = self.__es__.search(index=self.indexerstring, body={
            "sort": {"@timestamp": {"order": "desc"}},
            "query": {"filtered": {"filter": {"range": {"@timestamp": {"gte": self.timechecker}},},
                                              "query": {"match": {"grp": "workers"}}}},
            "aggs": {"query_value": {"stats": {"field": "val"}}},
            "size": 2500000
        })
        return elasticresult['aggregations']['query_value']

    def get_gunicorn_request_rate(self):
        """
        This function returns Average Request Rate from ElasticSearch
        """
        elasticresult = self.__es__.search(index=self.indexerstring, doc_type="counter", body={
            "sort": {"@timestamp": {"order": "desc"}},
            "query": {"filtered": {"filter": {"range": {"@timestamp": {"gte": self.timechecker}}},
                                              "query": {"match_all": {}}}},
            "aggs": {"query_value": {"stats": {"field": "val"}}},
            "size": 2500000
        })
        return elasticresult['aggregations']['query_value']

    def get_gunicorn_request_duration(self):
        """
        This function returns Average Request Duration from ElasticSearch
        """
        elasticresult = self.__es__.search(index=self.indexerstring, doc_type="timer_data", body={
            "sort": {"@timestamp": {"order": "desc"}},
            "query": {"filtered": {"filter": {"range": {"@timestamp": {"gte": self.timechecker}},},
                                              "query": {"match_all": {}}}},
            "aggs": {"query_value": {"stats": {"field": "mean"}}},
            "size": 2500000
        })
        return elasticresult['aggregations']['query_value']


class Gunicorn_Check(nagiosplugin.Resource):
    """
    This is the class to perform checks on Gunicorn. Constructor passes contextname
    casetype to this class for use by metric.
    """
    def __init__(self, returnval, contextname):
        self.gunicornstat = returnval
        self.contextname = contextname

    def probe(self):
        return [nagiosplugin.Metric(self.contextname, self.gunicornstat)]

class Run_Check(object):
    
    def __init__(self, datafetch):
        self.data_fetch = datafetch
        
    def run_check(self, contextname, gunicornstats, warning, critical):
        check = nagiosplugin.Check(Gunicorn_Check(gunicornstats, contextname),
                                   nagiosplugin.ScalarContext(contextname, warning, critical))
        check.main()

    def error_handler(self, contextname, warning, critical):
        return "This option is not available"

    # Workers with Max, Min and Average
    def max_worker(self, contextname, warning, critical):
        self.run_check(contextname, self.data_fetch.get_gunicorn_workers()['max'] , warning, critical)

    def min_worker(self, contextname, warning, critical):
        self.run_check(contextname, self.data_fetch.get_gunicorn_workers()['min'], warning, critical)

    def avg_worker(self, contextname, warning, critical):
        self.run_check(contextname, self.data_fetch.get_gunicorn_workers()['avg'], warning, critical)

    # Request Rate with Max, Min and Average
    def max_request_rate(self, contextname, warning, critical):
        self.run_check(contextname, self.data_fetch.get_gunicorn_request_rate()['max'], warning, critical)

    def min_request_rate(self, contextname, warning, critical):
        self.run_check(contextname, self.data_fetch.get_gunicorn_request_rate()['min'], warning, critical)

    def avg_request_rate(self, contextname, warning, critical):
        self.run_check(contextname, (self.data_fetch.get_gunicorn_request_rate()['avg']), warning, critical)

    # Request Durations with Max, Min and Average
    def max_request_duration(self, contextname, warning, critical):
        self.run_check(contextname, self.data_fetch.get_gunicorn_request_duration()['max'], warning, critical)

    def min_request_duration(self, contextname, warning, critical):
        self.run_check(contextname, self.data_fetch.get_gunicorn_request_duration()['min'], warning, critical)

    def avg_request_duration(self, contextname, warning, critical):
        self.run_check(contextname, self.data_fetch.get_gunicorn_request_duration()['avg'], warning, critical)
    
    

@nagiosplugin.guarded
def main():
    """
    This is the main function as name suggests. This function creates usable arguments
    to pass instructions to function as what it should do. Then function Checks the given casetype
    to get output to Nagios.
    """
    parser = argparse.ArgumentParser(description="G-Unicorn Nagios Plugin Help")
    parser.add_argument("-st", "--settime", type=int, default=5,
                        help="Set time range in minutes. Default time is 5 minutes")
    parser.add_argument("-t", "--casetype", type=str, default="maxworkers",
                        help="Select Your Case from 'RequestRate', 'RequestDuration', "
                             "and 'Workers'")
    parser.add_argument("-c", "--critical", type=str, default=":",
                        help="Set Critical Range.\n\t\ta:b for critical range outside "
                             "a and b where a and b are int\n\t\t@a:b for critical range "
                             "inside a and b where a and b are int")
    parser.add_argument("-w", "--warning", type=str, default=":",
                        help="Set warning Range.\n\t\ta:b for warning range outside a and b"
                             " where a and b are int\n\t\t@a:b for warning range inside a and b"
                             " where a and b are int")
    args = parser.parse_args()
    args.casetype = str(args.casetype).strip().capitalize()

    time_check = (int(time.time()-(60*args.settime)))*1000

    now = datetime.datetime
    index_name = 'statsd-'+str(now.today().year) + '.' + \
                    str(now.today().month)+'.'+str(now.today().day)
    if now.today().day < 10:
        index_name = 'statsd-'+str(now.today().year)+'.' \
                        + str(now.today().month)+'.0'+str(now.today().day)

    run_check = Run_Check(Gunicorn_Data_Fetch(time_check, index_name))

    case_types = {
        "Avgworkers": run_check.avg_worker,
        "Maxworkers": run_check.max_worker,
        "Minworkers": run_check.min_worker,
        "Avgrequestrate": run_check.avg_request_rate,
        "Maxrequestrate": run_check.max_request_rate,
        "Minrequestrate": run_check.min_request_rate,
        "Avgrequestduration": run_check.avg_request_duration,
        "Maxrequestduration": run_check.max_request_duration,
        "Minrequestduration": run_check.min_request_duration
    }
    case_types.get(args.casetype, run_check.error_handler )(args.casetype, args.warning, args.critical)

if __name__ == '__main__':
    main()