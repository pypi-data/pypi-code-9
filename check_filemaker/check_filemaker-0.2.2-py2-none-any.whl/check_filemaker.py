#!/usr/bin/env python
#
# Copyright (C) 2015 Real Time Enterprises, Inc.
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA
#
import sys, os, argparse
import getopt
from PyFileMaker import FMServer, FMServerError, FMError
from requests.exceptions import HTTPError
import ast

__here__ = os.path.abspath(os.path.dirname(__file__))
__version__ = open(os.path.join(__here__, 'version.txt')).read().strip()

__copyright__ = 'Copyright (C) 2015 Real Time Enterprises, Inc.'
__min_version__ = (2, 6)
__app_name__ = 'check_filemaker'
        
class CheckFilemaker:
    OK       = 0
    WARNING  = 1
    CRITICAL = 2
    UNKNOWN  = 3
    
    def connect(self, hostname, username, password, database, layout, debug = False):
        auth = username + ':' + password + '@' + hostname
        self._fm = FMServer(auth, database, layout)
        self._debug = debug
    
    def column(self, **params):
        return self._fm.doFind(params)
        
    def check_layouts(self, layouts):
        lays = self._fm.getLayoutNames()
        return set(lays) & set(layouts)
        
    def check_databases(self, databases):
        dbs = self._fm.getDbNames()
        return set(dbs) & set(databases)
        
def check_python():    
    if sys.version_info < __min_version__:
        print >> sys.stderr, 'Error: cannot find a suitable python interpreter'
        print >> sys.stderr, '  Need python %d.%d or later' % __min_version__
        print >> sys.stderr, '  Found python %d.%d' % (sys.version_info[0], sys.version_info[1])
        print >> sys.stderr, '  CRITICAL - Cannot find suitable python interpreter'
        raise SystemExit, CheckFilemaker.CRITICAL

def parse_cli(argv, release):
    
    parser = argparse.ArgumentParser(description='Nagios plugin to check status of Filemaker databases',
        epilog='Send email to tanner@real-time.com if you have questions regarding this software.')
    
    parser.add_argument('--version', action='version', version=release,
        help='print version information')
    parser.add_argument('-H', '--hostname', dest='hostname', required=True,
        help='Host name, IP Address')
    parser.add_argument('-d', '--database', dest='database', required=True,
        help='Check database with indicated name')
    parser.add_argument('-l', '--layout', dest='layout', required=True,
        help='Uses layout with indicated name')
    parser.add_argument('-c', '--column', dest='column', required=True, metavar='{"COLUMN":"VALUE"}',
        help='Look for {"COLUMN":"VALUE"} in the database')
    parser.add_argument('-u', '--username', dest='username', required=True,
        help='connect using the indicated username')
    parser.add_argument('-p', '--password', dest='password', required=True,
        help='use the indicated password to authenticate the connection')

    args = parser.parse_args()
    return args
       
if __name__ == "__main__":   
         
    try:     
        release = __app_name__ + ' ' + __version__

        check_python()
        args = parse_cli(sys.argv, release)
        
        fm = CheckFilemaker()
        
        hostname = args.hostname
        database = args.database
        layout = args.layout

        fm.connect(hostname, args.username, args.password, database, layout)
        
        dbs = [database]
        if fm.check_databases(dbs) != set(dbs):            
            raise Exception('Did not find the required database: ' + str(dbs))
            
        lays = [layout]
        if fm.check_layouts(lays) != set(lays):
            raise Exception('Did not find the required layout: ' + str(lays))
        
        # Literal evail of --column="{'Constant':'1'}" see 
        # http://stackoverflow.com/questions/988228/converting-a-string-to-dictionary
        #
        parm = ast.literal_eval(args.column)        
        column = fm.column(**parm)
        if len(column) <= 0:
            raise Exception('Did not find required column: ')
        
        print '%s OK - %s' % (release, database)    
        raise SystemExit, CheckFilemaker.OK
    except FMServerError as e:
        print 'CRITICAL - FMServerError: ', e
        raise SystemExit, CheckFilemaker.CRITICAL
    except FMError as e:
        print 'CRITICAL - FMError: ', e
        raise SystemExit, CheckFilemaker.CRITICAL
    except HTTPError as e:
        print 'CRITICAL - Invalid response from host: ', e
        raise SystemExit, CheckFilemaker.CRITICAL
    except KeyError as e:
        print 'CRITICAL - Missing required command line parameter:', e
        raise SystemExit, CheckFilemaker.CRITICAL
    except Exception as e:
        print type(e)
        print 'CRITICAL - Error: ', e
        raise SystemExit, CheckFilemaker.CRITICAL
