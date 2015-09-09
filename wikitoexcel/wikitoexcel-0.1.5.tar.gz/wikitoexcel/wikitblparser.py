'''

@author: venkman69
'''
from bs4 import BeautifulSoup
import re


class _tbl(object):
    attrs=None
    def __init__(self,attrs=None):
        self.attrs = attrs
    def __repr__(self):
        return str(self.attrs)

class wikiTbl(_tbl):
    rows=None
    caption=None
    def __init__(self,attrs=None):
        self.rows=[]
        self.caption=u""
        _tbl.__init__(self,attrs)
    
    def addRow(self,attrs=None):
        self.rows.append(wikiRow(attrs))
        return self.rows[-1]
    def setCaption(self,caption=u""): 
        self.caption=caption
        if self.caption==None:
            self.caption=""
    def __repr__(self):
        rep="TableStyle["+str(self.attrs) + "] Caption:["+self.caption+"]\n"
        for r in self.rows:
            rep+=" "+str(r)+"\n" 
        return rep

class wikiRow(_tbl):
    cells=None
    def __init__(self,attrs=None):
        self.cells=[]
        _tbl.__init__(self,attrs)

    def addCells(self,cells=[]):
        self.cells.extend(cells)
    
    def addCell(self,cell):
        self.cells.append(cell)

    def __repr__(self):
        rep="RowStyle["+str(self.attrs) + "]\n"
        for c in self.cells:
            rep+=" "+str(c)+"\n"
        return rep

class wikiCell(_tbl):
    text=None
    def __init__(self,text=None,attrs=None):
        if text==None:
            self.text=""
        else:
            self.text=text 
        _tbl.__init__(self,attrs)
    
    def appendText(self,txt):
        self.text += txt
        self.text = self.text.strip()
  
    def __repr__(self):
        return "CellStyle["+str(self.attrs)+"] cellValue="+self.text

def wikiAttrParse(wikiText,elementType):
    if wikiText == None:
        return {}
    tmpHTML="<%s %s>"%(elementType,wikiText)
    elem = BeautifulSoup(tmpHTML,"html.parser")
    styleAttrs= elem.find(elementType).attrs
    if styleAttrs.has_key("style") and styleAttrs["style"]!=u"":
        #separate this out
        sSplit=styleAttrs['style'].split(";")
        for k in sSplit:
            key,val = k.split(":")
            styleAttrs[key.strip()]=val.strip()
    return styleAttrs


def sepStyleAndValue(wikiText):
    wikiSplit = wikiText.split("|")
    if len(wikiSplit)==2:
        return wikiSplit[0],wikiSplit[1]
    else:
        return "",wikiText
    


def wikiTableParser(wikiText):
    """returns a list of 2d arrays of all cells within the wiki markup
    the cell contents themselves are raw contents of the wiki"""
    tblList=[]
    t=wikiText.split(u"\n")
    td = [] # Is currently a td tag open?
    ltd = [] # Was it TD or TH?
    tr = [] # Is currently a tr tag open?
    ltr = [] # tr attributes    
    tbl = [] # is a table open
    ltbl = [] # tbl attributes
    tblObj = None # current table object
    row=None
    cell=None
    for k, x in zip(range(len(t)),t):
        x=x.strip()
        fc=x[0:1]
        if x[0:2] == u"{|":
            attrText = x[2:]
            tblObj = wikiTbl(wikiAttrParse(attrText, "table"))
            continue
        if x[0:2] == u"|}":
            if cell!=None:
                row.addCell(cell)
            tblList.append(tblObj)
            tblObj=None
            continue
        if x[0:2] == u"|+":
            x=x[2:]
            cs,txt=sepStyleAndValue(x)
            tblObj.setCaption(txt)
            continue
        if x[0:2] == u"|-":
            x = x[2:]
            while x != u'' and x[0:1] == '-':
                x = x[1:]
            if cell!=None:
                row.addCell(cell)
            row=tblObj.addRow(wikiAttrParse(x, "tr"))
            cell=None
            continue
        if fc=="|" or fc=="!":
            x=x[1:]
            xsplit=x.replace(u"!!",u"||").split(u"||")
            for c in xsplit:
                styleStr,txt=sepStyleAndValue(c)
                cs=wikiAttrParse(styleStr, "td")
                #cell start
                if cell!=None:
                    row.addCell(cell)
                cell=wikiCell(txt,cs)

            continue
        else:
            if cell==None:
                print "No cell: ",x
            elif x!=None:
                # reinsert a new line since this would have been in another
                # line by coming here
                cell.appendText("\n"+x)
            
    return tblList
        

if __name__ == '__main__':
    with open("example/wikitbl.txt","r") as f:
        wikiTableParser(f.read())
    with open("example/etradewiki.txt","r") as f:
        wikiTableParser(f.read())