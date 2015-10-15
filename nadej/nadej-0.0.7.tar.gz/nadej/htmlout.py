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
def htmlFormat_h(elem):
    """
    """

    if "uuid" in elem : 
        href= "#%s"%elem["uuid"] 
    else:
        href= "" 
    return u"<%s id='%s'>%s</%s>"%(elem["type"],href,elem["text"],elem["type"])



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
        "h1":htmlFormat_h,
        "h2":htmlFormat_h,
        "h3":htmlFormat_h,
        "h4":htmlFormat_h,
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

BOOTSTRAP_META_FILTER = ["title","logo","summary"]


def htmlBootstrapFormater(dataList,inline=False):
    """
    """
    
        
    djson = json.dumps(dataList,indent=2,cls=JsonEscaper)
    
    meta={
        "title":u"No Title",
        "lead":u"",
        "summary":False
    }
    # preprocessing meta 
    for elem in dataList:
        if elem["type"] == "title":
            meta["title"]=elem["text"]
        if elem["type"] == "summary":
            meta["summary"]=True

    summary = bootstrapSummary(dataList)
    text= u"".join((bootstrapSwith(elem) for elem in dataList))

    if inline:
        return text
    else:
        from jinja2 import Template,Environment,PackageLoader
        #print os.path.realpath(__file__)
        env=Environment(loader=PackageLoader('nadej','templates'))
        env.filters['pdframetotable'] = pdframetotable_bs
        template = env.get_template('bootstraped.html')
        return template.render(d=dataList,djson=djson,meta=meta,text=text,summary=summary)

def bootstrapSummary(dataList):
    l = []
    current = 0
    
    def makeli(elem):
        import uuid
        elem["uuid"] = uuid.uuid4().hex
        return u"""<li class="list-unstyled">
                <a href="#%s">
                %s
                </a></li>"""%(
                elem["uuid"]    ,
                elem["text"]
            
            )

    def makeli2(elem):
        import uuid
        elem["uuid"] = uuid.uuid4().hex
        return u"""<a href="#%s">
                %s
                </a></li>"""%(
                elem["uuid"]    ,
                elem["text"]
            
            )
    
    for elem in dataList:
        if elem["type"] in ["h1","h2","h3","h4"]:

            hi = int(elem["type"][-1])

            if hi == current:
                l.append(makeli(elem))
            elif hi > current:
                # open new

                for _ in range(hi-current):
                    l.append("<ul>")
                    l.append("""<li class="list-unstyled">""")
                l.append(makeli2(elem))

                current = hi
            else :
                for _ in range(current-h1):
                    l.append("</ul>")

    for _ in range(current):
        l.append("</ul>")

    tmp = u"""
    <div class="panel">
        <div class="panel-heading">
          <h3 class="panel-title"></h3>
        </div>
        <div class="panel-body">
          %s
        </div>
    </div>
     """ 

    return tmp%( u"".join(l))


def bootstrapSwith(elem):
    if elem["type"] in ["h1","h2","h3","h4"]:
        return htmlFormat_h(elem)
    elif elem["type"] in ["p"]:
        return htmlFormat_p(elem)
    elif elem["type"] in ["img"]:
        return u"""<a href="#" class="thumbnail">
<div class="img-hover">
  <img class="img-responsive img-rounded" src="data:image/%s;base64,%s" alt="Embedded Image">
</div>
</a>"""%(elem["format"],elem["data"])
    elif elem["type"] in ["code"]:
        return u"""
        <pre><code class="%s">%s</code></pre>"""%(elem["format"],elem["text"])

    elif elem["type"] in ["table"]:
        if elem["format"] == "pd.frame":
            return pdframetotable_bs(elem["data"])






    elif elem["type"] in ["vsplit"]:
        mapping={
                2:6,
                3:4,
                4:3,
                6:2}
        return u"""
<div class="container">
<div class="row">
    <div class="col-md-%s">
        """%mapping[elem["count"]]

    elif elem["type"] in ["then"]:
        mapping={
                2:6,
                3:4,
                4:3,
                6:2}
        return u"""
    </div>
    <div class="col-md-%s">
        """%mapping[elem["count"]]
    elif elem["type"] in ["endsplit"]:
        return u"""
    </div>
</div><!-- /.row -->
</div><!-- /.container -->
        """
    elif elem["type"] in ["rst"]:
        from docutils.core import publish_parts

        return publish_parts(elem["text"],writer_name="html")['html_body']
        return "" 

    elif elem["type"] in ["test_text"]:

        if elem["success"]:
            return u"""
            <div class="alert alert-success" role="alert">
            %s
            </div>"""%elem["text"]

        else: 
            return u"""
            <div class="alert alert-danger" role="alert">
            %s
            </div>"""%elem["text"]
            pass
        
    elif elem["type"] in BOOTSTRAP_META_FILTER:
        return u""
    else:
        return u"<h1>NOTFOUND %s</h1>" % elem["type"]



