import os
import sys
from Automater.siteinfo import SiteFacade
from Automater.utilities import Parser, IPWrapper
from Automater.outputs import SiteDetailOutput
from Automater.inputs import TargetFile
import tempfile
import csv
from dbcache import dbcache

@dbcache
def robtex(indicator):
    automater_source = 'robtex'
    return get_automater_output(indicator, automater_source)

@dbcache
def fortinet_classify(indicator):
    automater_source = 'fortinet_classify'
    return get_automater_output(indicator, automater_source)

@dbcache
def vtpDNSIP(indicator):
    automater_source = 'vtpDNSIP'
    return get_automater_output(indicator, automater_source)

@dbcache
def ipvoid(indicator):
    automater_source = 'ipvoid'
    return get_automater_output(indicator, automater_source)

@dbcache
def virustotal(indicator):
    automater_source = 'virustotal'
    return get_automater_output(indicator, automater_source)

@dbcache
def threatexpert(indicator):
    automater_source = 'threatexpert'
    return get_automater_output(indicator, automater_source)

@dbcache
def vxvault(indicator):
    automater_source = 'vxvault'
    return get_automater_output(indicator, automater_source)

@dbcache
def unshortme(indicator):
    automater_source = 'unshortme'
    return get_automater_output(indicator, automater_source)

@dbcache
def urlvoid(indicator):
    automater_source = 'urlvoid'
    return get_automater_output(indicator, automater_source)

@dbcache
def vtpDNSDom(indicator):
    automater_source = 'vtpDNSDom'
    return get_automater_output(indicator, automater_source)

@dbcache
def malc0de(indicator):
    automater_source = 'malc0de'
    return get_automater_output(indicator, automater_source)

@dbcache
def ReputationAuthority(indicator):
    automater_source = 'ReputationAuthority'
    return get_automater_output(indicator, automater_source)

@dbcache
def FreeGeo(indicator):
    automater_source = 'FreeGeo'
    return get_automater_output(indicator, automater_source)

@dbcache
def SANS_API(indicator):
    automater_source = 'SANS API'
    return get_automater_output(indicator, automater_source)

@dbcache
def totalhash_ip(indicator):
    automater_source = 'totalhash_ip'
    return get_automater_output(indicator, automater_source)

@dbcache
def automater(indicator):
    '''Run an indicator through Automater as you would on the command line:
    `python Automater.py indicator` '''
    return get_automater_output(indicator, 'allsources')

def get_automater_output(indicator, source):
    fp = FakeParser()
    fp.source = source
    fp.target = indicator
    temp = tempfile.NamedTemporaryFile(delete=False)
    temp.close()
    fp.csv = temp.name
    run_automater(fp)
    automater_csv = open(temp.name, 'r')
    automater_out = {'indicator' : indicator}
    for r in csv.DictReader(automater_csv):
        if 'Result' not in r:
            automater_out['error'] = 'Automater error'
            continue
        source_name = r['Source'].replace(' ', '_').lower()
        result = r['Result']
        automater_out[source_name] = result
    temp.unlink(temp.name)
    return automater_out

def run_automater(fake_parser):
    sites = []
    parser =  fake_parser

    # if no target run and print help
    if parser.hasNoTarget():
        print '[!] No argument given.'
        parser.print_help()  # need to fix this. Will later
        sys.exit()

    # user may only want to run against one source - allsources
    # is the seed used to check if the user did not enter an s tag
    source = "allsources"
    if parser.hasSource():
        source = parser.Source

    # a file input capability provides a possibility of
    # multiple lines of targets
    targetlist = []
    if parser.hasInputFile():
        for tgtstr in TargetFile.TargetList(parser.InputFile):
            if IPWrapper.isIPorIPList(tgtstr):
                for targ in IPWrapper.getTarget(tgtstr):
                    targetlist.append(targ)
            else:
                targetlist.append(tgtstr)
    else:  # one target or list of range of targets added on console
        target = parser.Target
        if IPWrapper.isIPorIPList(target):
            for targ in IPWrapper.getTarget(target):
                targetlist.append(targ)
        else:
            targetlist.append(target)

    sitefac = SiteFacade()
    sitefac.runSiteAutomation(parser.Delay, parser.Proxy, targetlist, \
                              source, parser.hasPost(), parser.UserAgent)
    sites = sitefac.Sites
    if sites is not None:
        SiteDetailOutput(sites).createOutputInfo(parser)

class FakeParser(object):
    '''Because Automater is written in Java (albeit with Python syntax...) it
    constructs an elaborate, ridiculous, terrible Parser object from command-
    line arguments then passes that object around like crazy. This class
    implements the same interface but lets us set values like sane Python
    programmers would like.
    '''
    def __init__(self):
        self.cef = None
        self.web = None
        self.output = None
        self.csv = None
        self.delay = 2
        self.proxy = None
        self.target = None
        self.source = None
        self.p = None
        self.useragent = None

    def hasCEFOutFile(self):
        if self.cef:
            return True
        else:
            return False

    @property
    def CEFOutFile(self):
        if self.hasCEFOutFile():
            return self.cef
        else:
            return None


    def hasHTMLOutFile(self):
        if self.web:
            return True
        else:
            return False

    @property
    def HTMLOutFile(self):
        if self.hasHTMLOutFile():
            return self.web
        else:
            return None

    def hasTextOutFile(self):
        if self.output:
            return True
        else:
            return False

    @property
    def TextOutFile(self):
        if self.hasTextOutFile():
            return self.output
        else:
            return None

    def hasCSVOutSet(self):
        if self.csv:
            return True
        else:
            return False

    @property
    def CSVOutFile(self):
        if self.hasCSVOutSet():
            return self.csv
        else:
            return None

    @property
    def Delay(self):
        return self.delay

    def hasProxy(self):
        if self.proxy:
            return True
        else:
            return False

    @property
    def Proxy(self):
        if self.hasProxy():
            return self.proxy
        else:
            return None

    def print_help(self):
        pass
        #self._parser.print_help()

    def hasTarget(self):
        if self.target is None:
            return False
        else:
            return True

    def hasNoTarget(self):
        return not(self.hasTarget())

    @property
    def Target(self):
        if self.hasNoTarget():
            return None
        else:
            return self.target

    def hasInputFile(self):
        if os.path.exists(self.target) and os.path.isfile(self.target):
            return True
        else:
            return False

    @property
    def Source(self):
        if self.hasSource():
            return self.source
        else:
            return None

    def hasSource(self):
        if self.source:
            return True
        else:
            return False

    def hasPost(self):
        if self.p:
            return True
        else:
            return False

    @property
    def InputFile(self):
        if self.hasNoTarget():
            return None
        elif self.hasInputFile():
            return self.Target
        else:
            return None

    @property
    def UserAgent(self):
        return self.useragent
