'''
Created on Aug 18, 2015

@author: venkman69
'''
from copy import deepcopy
import re

import bs4
from bs4 import BeautifulSoup
from openpyxl import Workbook
from openpyxl.styles import fills
from openpyxl.styles.colors import Color
from openpyxl.styles.fills import PatternFill
from openpyxl.styles.fonts import Font
from openpyxl.styles.alignment import Alignment
from openpyxl.utils import coordinate_from_string
from wikimarkup import parse
from __builtin__ import file
import os


# import getpass
def getHTMLStyle(htmlNode):
    pass

def captionToExcel(capNode):
    # this is worksheet name
    return capNode.text.strip()

def procHTMLLists(htmlNode):        
    wikiStr=""
    prefix=""
    if htmlNode.name.lower() == "ul":
        prefix="*"
    if htmlNode.name.lower() == "ol":
        prefix="#"
    for cNode in htmlNode.children:
        wikiStr+= prefix + cNode.text
    return wikiStr

def procHTMLLink(htmlNode):
    wikiStr=""
    url=htmlNode['href']
    displayText= htmlNode.text
    wikiStr+=url + " " + displayText
    return wikiStr

def procSpanDiv(htmlNode):
    return htmlNode.text

def procStyle(bsNode):        
    """proc style only retrieves the following style items:
    - font size
    - font weight (bold)
    - font color
    - font strikethrough
    - font underline
    - font italics
    - background color
    """
    procstyles=['font-weight',
                'font_name',
                'italic',
                'line-through',
                'underline',
                'background-color',
                'width',
                'color']
    if not bsNode.has_attr('style'):
        return None
    styleMap=dict((k,False) for k in procstyles)
    for styleKV in  bsNode['style'].split(';'):
        styleKVList=styleKV.split(":")
        k=styleKVList[0].strip().lower()
        v=styleKVList[1].strip().lower()
        if k == "font-family":
            styleMap['font_name']=v
        if k == "font-weight":
            if v=="bold":
                styleMap["bold"]=True
        if k == "color":
            styleMap["color"]=v
        if k == "text-decoration":
            if v in ['underline', 'line-through']:
                styleMap[v]=True
        if k == "font-style":
            if v=="italic":
                styleMap[v]=True
        if k == 'width':
            if v != "":
                styleMap['width']=v
        if k == "background-color" and v != False:
            styleMap['background-color']=v

    return styleMap

def applyFmt(tblStyle, trStyle,tdStyle, cell,ws):
    # resolve all the styles
    finalStyle=deepcopy(tblStyle)
    if finalStyle == None:
        finalStyle ={}
    for s in [trStyle,tdStyle]:
        if s==None:
            continue
        for k,v in s.iteritems():
            if v == False:
                continue
            finalStyle[k]=v
    font=Font()
    for k,v in finalStyle.iteritems():
        if k == "italic" and v!=False:
            font.i=True
        if k == "underline" and v!=False:
            font.u=Font.UNDERLINE_SINGLE
        if k == "line-through" and v!=False:
            font.strikethrough=True
        if k == "font_name" and v!=False:
            font.name=v
        if k=="bold" and v==True:
            font.bold=True
        if k=='width' and v != "" and v != False:
            c,r=coordinate_from_string(cell.coordinate)
            m=re.match("([\d\.]+)(\D+)",v)
            if m != None:
                w=m.group(1)
                units=m.group(2)
                if units == "in":
                    w=float(w)*12
            ws.column_dimensions[c].width=w
        if k == "color" and v != False:
            font.color = v[1:]
        if k == "background-color" and v != False:
            c=Color(v[1:])
            fill=PatternFill(patternType=fills.FILL_SOLID,fgColor=c)
            cell.fill = fill
            
    cell.font=font        

def trToExcel(ws,tr,rowCount,tblStyle):
    trStyle = procStyle(tr)
    colCount=1
    tdthList=tr.findAll('td')
    if len(tdthList)==0:
        tdthList=tr.findAll('th')

    for td in tdthList:
        rowspan,colspan, colMergeOffset=tdToExcel(ws,td,colCount,rowCount,trStyle,tblStyle)
        colCount+=1+colspan+colMergeOffset

def tdToExcel(ws,td,colCount, rowCount, trStyle, tblStyle): 
    procMap={'ol':procHTMLLists,
             'ul':procHTMLLists,
             'span':procSpanDiv,
             'a':procHTMLLink,
             'p':lambda x: x.text,
             }
    colspan=0
    rowspan=0
    colMergeOffset=0
    tdStyle = procStyle(td)
    cell=ws.cell(column=colCount,row=rowCount)
    while cell.coordinate in ws.merged_cells:
        colMergeOffset+=1
        cell=ws.cell(column=colCount+colMergeOffset,row=rowCount)

    tdcontents=""
    for child in td.children:
        if child.name == None or len(child.contents)==0:
            if isinstance(child, bs4.element.NavigableString):
                tdcontents+=child
            elif child.text != "":
                tdcontents+=child.text
            continue
        if len(child.contents)> 1 and child.name == "p":
            for cc in child.children:
                if cc.name == None:
                    continue
                if procMap.has_key(cc.name.lower()):
                    tdcontents +=procMap[cc.name.lower()](cc)
        elif procMap.has_key(child.name.lower()):
            tdcontents +=procMap[child.name.lower()](child)
        else:
            print "not found",child.name.lower()
    tdcontents = tdcontents.strip()
    cell.value=tdcontents
    # if line contains multiple lines, then set the wrap style on
    # this means return character exists between texts
    print "[%s]"%tdcontents, re.search(r"\w+\r\w+", tdcontents)
    if re.search(r".+\n.+", tdcontents):
        cell.alignment = Alignment(wrapText=True)
        print "Wrap:",cell.coordinate

    if td.has_attr('colspan'):
        colspan+=int(td['colspan']) -1
    if td.has_attr('rowspan'):
        rowspan=int(td['rowspan']) -1
    if colspan != 0 or rowspan != 0:
        ws.merge_cells(start_row=rowCount,start_column=colCount,
                       end_row=rowCount+rowspan, end_column=colCount+colspan)
    
    applyFmt(tblStyle,trStyle,tdStyle,cell,ws)
    
    
    return rowspan, colspan, colMergeOffset
    


def htmlToExcel(htmlContent):
    cdom=BeautifulSoup(htmlContent)
    tblCount=0
    wb=Workbook()
    for tbl in cdom.find_all("table"):
        caption=tbl.find("caption")
        tblCount+=1
        if caption != None:
            shtName=captionToExcel(caption)
        else:
            shtName = "Sheet"+str(tblCount)

        ws=wb.create_sheet(tblCount, shtName)
        # set the new sheet as active
        wb.active=wb.get_index(ws)
        tblStyle=procStyle(tbl)
        rowCount=1
        for tr in tbl.findAll("tr"):
            trToExcel(ws,tr,rowCount,tblStyle)
            rowCount+=1
    return wb

class wikiToExcel():
    wb=None
    htmlContent=None
    def __init__(self,wikiContent=None,infile=None, ):
        """wikiContent is a string containing the wiki text
        or infile can be a filepath or a file-like object """

        if wikiContent != None:
            self.htmlContent= parse(wikiContent)
        elif infile != None:
            if isinstance(infile, file):
                self.htmlContent= parse(infile.read())
            elif os.path.exists(infile):
                with open(infile,"r") as wikiFile:
                    self.htmlContent= parse(wikiFile.read())
            else:
                raise ValueError("Input file or path is required: %s"%infile)
        else:
            raise ValueError("Insufficient arguments")
        self.wb= htmlToExcel(self.htmlContent)
    
    def getHTML(self):
        return self.htmlContent

    def getWorkBook(self):
        return self.wb
    
    def saveExcel(self,fileObj=None,fileName=None):
        """fileObj is a file like object
        fileName is path and name of file to write 
        one of the two should be present"""
        import sys
        if fileObj != None:
            try:
                self.wb.save(fileObj)
            except:
                print sys.exc_info()
                raise Exception("Could not save excel to: %s"%fileObj)
        elif fileName != None:
            with open(fileName,"w") as fileObj:
                try:
                    self.wb.save(fileObj)
                except:
                    print sys.exc_info()
                    raise Exception("Could not save excel to: %s"%fileName)
                
                
