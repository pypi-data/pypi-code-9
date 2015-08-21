
from pylookwhat import patch

if __name__=='__main__':
    import sys
    for i in xrange( len(sys.argv) ):
        param = sys.argv[i]
        if param == 'patch' and len(sys.argv) >= (i+2):
            backupTarget = True
            targetName = sys.argv[i+1]
            sourceName = sys.argv[i+2]
            if len( sys.argv ) > (i+3):
                backupTarget = sys.argv[i+3].lower() not in ('false', '0', 'no')
            patch(  targetName, sourceName, backupTarget )
