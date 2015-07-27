import argparse
import configparser
from sharepointcacheprimer import primer

def execute(argv=None):
    parser = argparse.ArgumentParser(description="""Connect to sharepoint site, 
        authenticate, and load a page, thereby priming the caches.  The 
        configuration file should contain a section defining each site you are
        priming.
        """)
    parser.add_argument("config", 
        help="configuration ini file")
    parser.add_argument("site", 
        help="sites (section names) in configuration ini file to prime",
        nargs="+")
    args = parser.parse_args(argv)

    config = configparser.ConfigParser()
    config.optionxform = str
    config.read(args.config)

    sessions = []
    for site in args.site:
        if site in config:
            siteconf = config[site]
            #cookielist = {}
            if 'cookielist' in siteconf:
                for cookieset in config[siteconf['cookielist']].items():
                    #cookielist[cookieset[0]] = []
                    for cookie in cookieset[1].split(','):
                        #cookielist[cookieset[0]].append(cookie)
                        sessions.append(primer.Session(url=siteconf['url'],
                            username=siteconf['username'],
                            password=siteconf['password'],
                            cookie={cookieset[0]: cookie},
                            ))
            else:
                sessions.append(primers.Session(url=siteconf['url'], 
                    username=siteconf['username'], 
                    password=siteconf['password'], 
                    ))
        else:
            #error
            pass

    for session in sessions:
        session.prime_cache()
        print("{}: {}".format(session, session.state))