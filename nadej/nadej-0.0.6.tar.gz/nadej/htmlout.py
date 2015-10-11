# -*- coding: utf-8 -*-
import json
import os
def htmlFormater(dataList):
    """


    """
    
    headArray=[]
    bodyArray=[]
    for elem in dataList:

        if elem["type"] == "title":
            res=htmlFormat_title(elem)

            headArray.append(res)
        else:

            res=HTMLFORMAT_DIC[elem["type"]](elem)
            bodyArray.append(res)

    headText = u"<head> %s  </head>"%(u" ".join(headArray))
    
    bodyText = u"<body>%s</body>"%(u" ".join(bodyArray),)



    return u"""<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
<html>
%s 
%s
</html>"""%(
            headText,
            bodyText
            )

def htmlInlineFormater(dataList):
    """

    """
    bodyArray=[]
    for elem in dataList:
        if elem["type"] == "title":
            pass
        else:
            res=HTMLFORMAT_DIC[elem["type"]](elem)
            bodyArray.append(res)
    return u" ".join(bodyArray)

def htmlFormat_table(elem):
    """
    """
    import pandas as pd
    if elem["format"] == "pd.frame":
        return elem["data"].to_html()
    else:
        raise Exception("elem format not supported %s"%(elem["format"]))
def htmlFormat_title(elem):
    """
    """
    return u"<title>%s</title>"%elem["text"]
def htmlFormat_h1(elem):
    """
    """
    return u"<h1>%s</h1>"%elem["text"]
def htmlFormat_h2(elem):
    """
    """
    return u"<h2>%s</h2>"%elem["text"]
def htmlFormat_img(elem):
    """
    """

    if elem["format"] == "png":

        return u"""
    <img alt="Embedded Image" 
        src="data:image/png;base64,%s" />
"""%(elem["data"])

def htmlFormat_code(elem):
    """
    """
    return u"<pre>%s</pre>"%elem["text"]

def htmlFormat_p(elem):
    """
    """
    return u"<p>%s</p>"%elem["text"]


HTMLFORMAT_DIC = {
        "h1":htmlFormat_h1,
        "h2":htmlFormat_h2,
        "title":htmlFormat_title,
        "img":htmlFormat_img,
        "p":htmlFormat_p,
        "code":htmlFormat_code,
        "table":htmlFormat_table,

        }







class JsonEscaper(json.JSONEncoder):
    def default(self,obj):
        return u"ErrorJSON"

def pdframetotable_bs(df):
    from bs4 import BeautifulSoup
    soup = BeautifulSoup(df.to_html(), 'html.parser')
    table = soup.find_all("table")[0]

    res = soup.find_all("table")[0]
    newclassset = res["class"]+['table table-bordered table-condensed table-hover']

    res["class"] = newclassset
    return soup.prettify()


def htmlBootstrapFormater(dataList,inline=False):
    """
    """
    from jinja2 import Template,Environment,PackageLoader
    #print os.path.realpath(__file__)
    env=Environment(loader=PackageLoader('nadej','templates'))
    env.filters['pdframetotable'] = pdframetotable_bs
    
    if inline:
        template = env.get_template('bsinlined.html')
    else:
        template = env.get_template('bootstraped.html')
        
    djson = json.dumps(dataList,indent=2,cls=JsonEscaper)
    
    title = u"No Title"

    for elem in dataList:
        if elem["type"] == "title":
            title=elem["text"]


    meta={
            "title":title,
            "lead":u""
            }
    return template.render(d=dataList,djson=djson,meta=meta)






