'''
Created on Aug 26, 2015

@author: venkman69@yahoo.com
'''

from wikitoexcel import wikiToExcel
w2e = wikiToExcel(infile="./wikitbl.txt")
from StringIO import StringIO

sbuf = StringIO()

w2e.saveExcel(fileObj=sbuf)
w2e.saveExcel(fileName="out.xlsx")
