
import re
from copy import deepcopy
import ast


_branchs=[
    ['{','}', 0 ],
    ['"','"', 0 ],
    ['[',']', 0 ],
    ['\'','\'', 0 ],
]


def lookwhat( filename, res, nameList ):
    pt = re.compile( r'\s*(\w+)\s*=([^=\n]*)' )
    ptcomm = re.compile( '#[^\n]*' )

    usebranch = deepcopy( _branchs )

    rslt = res
    pstep = 0
    psname = ''
    templines = []
    try:
        f = open( filename, 'r' )
        fc = f.readlines()
        inComment1 = False
        inComment2 = False
        for line in fc:
            line = ptcomm.sub( '', line )  # remove comment
            if pstep == 0:
                m = pt.match( line )
                if m and not (inComment1 or inComment2):
                    name = m.groups()[0]
                    if name in nameList:
                        pstep = 1
                        psname = name    
                        line = line[ line.find('=')+1 : ]
                        usebranch = deepcopy( _branchs )
                else:
                    if line.find( "'''" ) >=0:
                        inComment1 = not inComment1
                    if line.find( '"""' ) >=0:
                        inComment2 = not inComment2
            if pstep == 1:
                for c in line:
                    for b in usebranch:
                        if c == b[0]:
                            b[2] += 1
                        if c == b[1]:
                            b[2] -= 1
                nb = False
                for b in usebranch:
                    if b[2] !=0:
                        nb = True
                        break
                templines.append( line )#.strip() # remove newline
                if not nb:
                    pstep = 2

            if pstep == 2:
                #dtext = templines 
                dtext = psname + '='+ "".join(templines)
                #print( dtext )
                g = {} 
                l = {}
                #u = eval( dtext, g, l )
                #g = ast.literal_eval( dtext )
                exec( dtext, g, l )
                fvar = rslt.get( psname )
                g = l.get(psname)
                if fvar:
                    fvar.update( g )
                else:
                    rslt[psname] = g
                    
                pstep = 0
                templines = []
                psname = ''
                


    finally:
        if f:
            f.close()
    return rslt



def _do_patch( targetName, newVariables ):
    import pprint
    pt = re.compile( r'\s*(\w+)\s*=([^=\n]*)' )
    ptcomm = re.compile( '#[^\n]*' )

    usebranch = deepcopy( _branchs )
    nameList = newVariables.keys()

    rslt = newVariables
    pstep = 0
    psname = ''
    newFileContent = []
    f = None
    try:
        f = open( targetName, 'r' )
        fc = f.readlines()
        f.close()
        inComment1 = False
        inComment2 = False
        for lineTarget in fc:
            line = ptcomm.sub( '', lineTarget )  # remove comment
            if pstep == 0:
                m = pt.match( line )
                if m and not (inComment1 or inComment2 ):
                    name = m.groups()[0]
                    if name in nameList:
                        pstep = 1
                        psname = name    
                        line = line[ line.find('=')+1 : ]
                        usebranch = deepcopy( _branchs )
                else:
                    if line.find( "'''" ) >=0:
                        inComment1 = not inComment1
                    if line.find( '"""' ) >=0:
                        inComment2 = not inComment2

                    newFileContent.append( lineTarget )
            if pstep == 1:
                for c in line:
                    for b in usebranch:
                        if c == b[0]:
                            b[2] += 1
                        if c == b[1]:
                            b[2] -= 1
                nb = False
                for b in usebranch:
                    if b[2] !=0:
                        nb = True
                        break
                
                if not nb:
                    pstep = 2

            if pstep == 2:
                newVar = newVariables.get( psname )
                newCt = psname + ' = ' + pprint.pformat( newVar, indent=4 ) 
                print newCt
                newFileContent.append( newCt +'\n' )
                    
                pstep = 0
                psname = ''
        
        f = open( targetName, 'w' )
        f.writelines( newFileContent ) # missing empty line
        f.close()


    except Exception as e:
        print str(e)
    return rslt

def patch( targetName, sourceName, backupTarget ):
    import datetime
    from os import path
    import shutil

    fsource = open( sourceName, 'r' )
    srcContexnt = fsource.read()
    fsource.close()
    g = {}
    l = {}
    exec( srcContexnt, g, l )
    if backupTarget:
        suffix = datetime.datetime.now().strftime( "%Y%m%d%H%M%S" )
        shutil.copyfile( targetName, "%s.%s"% (targetName, suffix) )
    _do_patch( targetName, l )



# Other two ways to get values
# 1. use single line parse with ast.literal_eval
# 2. use exec and get from local variables




    