#!/usr/local/bin/python2.7
# encoding: utf-8
"""
runner.raw_data_cli -- shortdesc

runner.raw_data_cli is a description

It defines classes_and_methods

@author:     Jason Bowles

@copyright:  2015 organization_name. All rights reserved.

@license:    license

@contact:    jaykbowles@gmail.com
@deffield    updated: Updated
"""

import sys
import os
import re

from argparse import ArgumentParser
from argparse import RawDescriptionHelpFormatter
from rawdata_emca.runner.raw_processor import RawProcessor


__all__ = []
__version__ = 0.1
__date__ = '2015-02-11'
__updated__ = '2015-02-11'

DEBUG = 0
TESTRUN = 0
PROFILE = 0

class CLIError(Exception):
    """Generic exception to raise and log different fatal errors."""
    def __init__(self, msg):
        super(CLIError).__init__(type(self))
        self.msg = "E: %s" % msg
    def __str__(self):
        return self.msg
    def __unicode__(self):
        return self.msg

def process_files(files, run_date=None, force_entry=None, log_file=None):
    params = {'files':files}
    if run_date:
        params['run_date'] = run_date
    if log_file:
        params['log_file'] = log_file    
    if force_entry:
        params['force'] = force_entry

    rp = RawProcessor(params)
    return rp.execute_entries()
        
        
def main(argv=None): # IGNORE:C0111
    """Command line options."""

    if argv is None:
        argv = sys.argv
    else:
        sys.argv.extend(argv)

    program_name = os.path.basename(sys.argv[0])
    program_version = "v%s" % __version__
    program_build_date = str(__updated__)
    program_version_message = '%%(prog)s %s (%s)' % (program_version, program_build_date)
    #program_shortdesc = __import__('__main__').__doc__.split("\n")[1]
    program_shortdesc = "Runs the config files in passed in directory"
    program_license = """%s

  Created by user_name on %s.
  Copyright 2015 organization_name. All rights reserved.

  Licensed under the Apache License 2.0
  http://www.apache.org/licenses/LICENSE-2.0

  Distributed on an "AS IS" basis without warranties
  or conditions of any kind, either express or implied.

USAGE
""" % (program_shortdesc, str(__date__))

    try:
        # Setup argument parser
        parser = ArgumentParser(description=program_license, formatter_class=RawDescriptionHelpFormatter)
        parser.add_argument("-r", "--recursive", dest="recurse", action="store_true", help="recurse into subfolders [default: %(default)s]")
        parser.add_argument("-v", "--verbose", dest="verbose", action="count", help="set verbosity level [default: %(default)s]")
        parser.add_argument("-i", "--include", dest="include", help="only include paths matching this regex pattern. Note: exclude is given preference over include. [default: %(default)s]", metavar="RE" )
        parser.add_argument("-e", "--exclude", dest="exclude", help="exclude paths matching this regex pattern. [default: %(default)s]", metavar="RE" )
        parser.add_argument('-V', '--version', dest="version", action='version', version=program_version_message)
        parser.add_argument('-t', '--test', dest='test_mode', action='store_true', help="Are we running the test version")
        parser.add_argument('-f', '--force', dest='force_run', action='store', help="force run an entry")
        parser.add_argument('-d', '--rundate', dest='run_date', action="store", help='Optional run date.. if not sent.. defaults to today(s) date.')
        parser.add_argument('-l', '--logfile', dest='log_file', action='store', help='specify the log file location')
        parser.add_argument(dest="paths", help="paths to folder(s) with source file(s) [default: %(default)s]", metavar="path", nargs='+')

        # Process arguments
        args = parser.parse_args()

        paths = args.paths
        test_mode = 0
        run_date = None
        force_entry = None
        log_file = None
        if hasattr(args, 'test_mode'):
            test_mode = args.test_mode
            
        if hasattr(args, 'force_run'):
            force_entry = args.force_run
        
        if hasattr(args,'run_date'):
            run_date = args.run_date
            
        if hasattr(args,'log_file'):
            log_file = args.log_file
            
        verbose = args.verbose
        recurse = args.recurse
        inpat = args.include
        expat = args.exclude
        
        if test_mode > 0:
            verbose = 1
            inpat = '^[tT][eE][sS][tT].*\.(cfg)$'
        

        if verbose > 0:
            print("Verbose mode on")
            if recurse:
                print("Recursive mode on")
            else:
                print("Recursive mode off")

        if inpat and expat and inpat == expat:
            raise CLIError("include and exclude pattern are equal! Nothing will be processed.")
        
        if not inpat and not expat:
            inpat = ".*\.(cfg)$"
        
        files = []
        for inpath in paths:
            ### do something with inpath ###                
            file_list = os.listdir(inpath)
            for f in file_list:
                match = False
                if inpat:
                    rein = re.compile(inpat)
                    if rein.match(f):
                        match = True
                if expat:
                    reex = re.compile(expat)
                    if reex.match(f):
                        match = False
                if match:
                    files.append(os.path.join(inpath, f))
                    
        aret = process_files(files,run_date, force_entry, log_file)
        print "Raw Data Running has been completed... "
        return aret
    except KeyboardInterrupt:
        ### handle keyboard interrupt ###
        return 0
    except Exception, e:
        #if DEBUG or TESTRUN:
        ##    import traceback
        #    traceback.print_exc()
        #    raise(e)
        import traceback
        traceback.print_exc()
        indent = len(program_name) * " "
        sys.stderr.write(program_name + ": " + repr(e) + "\n")
        sys.stderr.write(indent + "  for help use --help")
        
        return 2

if __name__ == "__main__":
    if DEBUG:
        sys.argv.append("-h")
        sys.argv.append("-v")
        sys.argv.append("-r")
    if TESTRUN:
        import doctest
        doctest.testmod()
    if PROFILE:
        import cProfile
        import pstats
        profile_filename = 'runner.raw_data_cli_profile.txt'
        cProfile.run('main()', profile_filename)
        statsfile = open("profile_stats.txt", "wb")
        p = pstats.Stats(profile_filename, stream=statsfile)
        stats = p.strip_dirs().sort_stats('cumulative')
        stats.print_stats()
        statsfile.close()
        sys.exit(0)
    sys.exit(main())