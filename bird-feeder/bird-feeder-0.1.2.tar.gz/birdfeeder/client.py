import pysolr
import threddsclient
from . parser import ThreddsParser, NetCDFParser

import logging
logger = logging.getLogger(__name__)


def clear(service):
    solr = pysolr.Solr(service, timeout=10)
    logger.info("deletes all datasets from solr %s", service)
    solr.delete(q='*:*')
   

def feed_from_thredds(service, catalog_url, depth=1, maxrecords=-1, batch_size=50000):    
    logger.info("solr=%s, thredds catalog=%s", service, catalog_url)
    publish(service, parser=ThreddsParser(catalog_url, depth), maxrecords=maxrecords, batch_size=batch_size)
    
    
def feed_from_directory(service, start_dir, maxrecords=-1, batch_size=50000):
    logger.info("solr=%s, start dir=%s", service, start_dir)
    publish(service, parser=NetCDFParser(start_dir), maxrecords=maxrecords, batch_size=batch_size)


def publish(service, parser, maxrecords=-1, batch_size=50000):    
    solr = pysolr.Solr(service, timeout=10)

    records = []
    for metadata in parser.crawl():
        records.append(metadata)
        if len(records) >= batch_size:
            # publish if batch size is reached
            logger.info("publish %d records", len(records))
            solr.add(records)
            records = [] # reset records
        elif maxrecords >=0 and len(records) >= maxrecords:
            # stop publishing if max records reached
            break
    logger.info("publish %d records", len(records))
    solr.add(records)


