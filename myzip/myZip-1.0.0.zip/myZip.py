# -*- coding: utf-8 -*
# Filename: myZip.py

__author__ = 'Piratf'

import os, sys
import zipfile

def zipFiles2TargetPath(sourcePath, targetPath, exclude = []):
    ''' zip files in sourcePath, recursively

    the zip file will be put in the targetPath,
    if you want to exclude some folders in the sourcePath, list them in the third parameter.
    using zipfile in the standard library'''
    print ("start zip")
    filesCount = 0;
    f = zipfile.ZipFile(targetPath, 'w', zipfile.ZIP_DEFLATED)
    for dirpath, dirnames, filenames in os.walk( sourcePath ):
        for excludePath in exclude:
            if excludePath in dirnames:
                dirnames.remove(excludePath)
        for filename in filenames:
            filesCount += 1;
            # at here we will report the process
            print ('dealing %s\r' % filesCount, end = '')
            sys.stdout.flush()
            f.write(os.path.join(dirpath, filename))
    f.close()
    print ("zip completed")
    return filesCount