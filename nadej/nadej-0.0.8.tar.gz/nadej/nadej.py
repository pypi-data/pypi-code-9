# -*- coding: utf-8 -*-

import os
from StringIO import StringIO
from  htmlout import htmlInlineFormater,htmlBootstrapFormater,htmlFormater

import json


def savein(data,dest):
    """

    save data in html
    """
    if os.path.isabs(dest):
        with open(dest,"w") as ou:
            ou.write(data)
    
    if dest.endswith(".html"):
        with open(dest,"w") as ou:
            ou.write(data)
    else:
        raise Exception ("Format not accepted")
class ClientAPI(object):

    def __init__(self):
        self.dataList=[]

        self.state=[]

    def title(self,text=""):
        """
        Clean up buffer
        """
        self.dataList=[]
        dic = {"type":"title",
                "text":text}
        self.dataList.append(dic)
    def summary(self,text="",shift=2,limit=3):
        """
        """
        dic = {"type":"summary",
                "text":text,
                "shift":shift,
                "limit":limit}

        self.dataList.append(dic)
    def lead(self,text=""):
        """
        below title
        """
        dic = {"type":"lead",
                "text":text}

        self.dataList.append(dic)
    def h1(self,text=""):
        """
        """

        dic = {"type":"h1",
                "text":text}
        self.dataList.append(dic)
        

    def h2(self,text=""):
        """
        """
        dic = {"type":"h2",
                "text":text}
        self.dataList.append(dic)
    def h3(self,text=""):
        """
        """
        dic = {"type":"h3",
                "text":text}
        self.dataList.append(dic)
    def h4(self,text=""):
        """
        """
        dic = {"type":"h4",
                "text":text}
        self.dataList.append(dic)
    
    #def prst(self,text=""):
    #    """
    #    Insert rst paragraph rst with be translated in html.
    #    """
    #    dic = {"type":"h3",
    #            "text":text}
    #    self.dataList.append(dic)
    
    def precode(self,text="",formt=""):
        """
        Insert preformated code section
        """
        dic = {"type":"code",
            "format":formt,
            "text":text}
        self.dataList.append(dic)

    def json(self,text=""):
        if isinstance(text,(dict,list)):
            dic = {"type":"code",
                "format":"json",
                "text":json.dumps(text,indent=2)}
            self.dataList.append(dic)

        elif isinstance(text,basestring):
            dic = {"type":"code",
                "format":"json",
                "text":text}
            self.dataList.append(dic)


    def text(self,text=""):
        """
        """
        dic = {"type":"p",
                "text":text}
        self.dataList.append(dic)

    def table(self,data=""):
        """
        """
        import pandas as pd
        dic = {"type":"table",
                "format":"pd.frame",
                "data":data
                }
        self.dataList.append(dic)
    def png(self,data):
        """
        data should be base64
        """
        dic = {"type":"img",
               "format":"png",
               "data":data}
        self.dataList.append(dic)
    
    def rst(self,text):
        """
        """
        dic = {"type":"rst",
               "text":text}

        self.dataList.append(dic)
    def logo(self,data,formt='png'):
        """

        """
        dic = {"type":"logo",
               "format":formt,
               "data":data}
        self.dataList.append(dic)

    def plot(self,data=""):
        """
        """
        import pandas as pd

        if isinstance(data,pd.DataFrame):
            import matplotlib
            #matplotlib.use('Agg')
            import matplotlib.pyplot as plt
            fig = plt.figure()
            for col in data:
                plt.plot(data.index,data[col],marker="o",label=col,)

            ymax,ymin = data.max().max(),data.min().min()
            ampli = (ymax-ymin)*0.05
            plt.ylim([ymin-ampli,ymax+ampli])

            xmax,xmin = data.index.max(),data.index.min()
            ampli = (xmax-xmin)/10
            plt.xlim([xmin-ampli,xmax+ampli])

            if isinstance(data.index,pd.DatetimeIndex):
                fig.autofmt_xdate()
            plt.legend()

            bufferIMG = StringIO()
            plt.savefig(bufferIMG)
            # out put as png
            from base64 import b64encode,b64decode
            buffer64 = b64encode(bufferIMG.getvalue())

            self.png(buffer64)
        elif isinstance(data,pd.Series):
            import matplotlib
            #matplotlib.use('Agg')
            import matplotlib.pyplot as plt
            fig = plt.figure()
            plt.axis=('tight')
            ax1 = plt.plot(data.index,data,marker="o",label=data.name)
            
            ymax,ymin = data.max(),data.min()
            ampli = (ymax-ymin)*0.05
            plt.ylim([ymin-ampli,ymax+ampli])
            
            xmax,xmin = data.index.max(),data.index.min()
            ampli = (xmax-xmin)/10
            plt.xlim([xmin-ampli,xmax+ampli])

            #ax1.set_ylim([-10,10])
            if isinstance(data.index,pd.DatetimeIndex):
                fig.autofmt_xdate()
            plt.legend()

            bufferIMG = StringIO()
            plt.savefig(bufferIMG)
            # out put as png
            from base64 import b64encode,b64decode
            buffer64 = b64encode(bufferIMG.getvalue())

            self.png(buffer64)

        else:
            raise Exception("not supported yet")
    def split(self,act="vsplit",count=1):
        """
        If act is 

        * vsplit: it starts a vertical Split
        * end: it ends the last opened element

        """
        
        if act == "vsplit":
            dic = {"type":"vsplit",
                    "count":count}
            self.dataList.append(dic)
            self.state.append(dic)
        elif act == "end":
            if len(self.state) >0:
                elem = self.state.pop()
                if elem["type"] == "vsplit":
                    dic = {"type":"endsplit",}
                    self.dataList.append(dic)
                else:
                    raise Exception("State Error")
            else:
                raise Exception("State Error, should find something")
    

    def then(self):
        """
        close the last opened element
        """
        #previousCount = self.state[-1]["count"]
        #newcount = previousCount+1
        #self.state[-1]["count"] = newcount
        count =self.state[-1]["count"] 
        
        dic = {"type":"then","count":count}
        self.dataList.append(dic)
    
    def test_s(self,text=u''):
        """
        test success
        """
        dic= {"type":"test_text",
                "success": True,
                "text":text}
        self.dataList.append(dic)

    def test_f(self,text=u''):
        """
        test success
        """
        dic= {"type":"test_text",
                "success": False,
                "text":text}
        self.dataList.append(dic)

    def collect(self,outpipe=""):
        """
        """
        ret = self.dataList
        self.dataList=[]

        if outpipe == "":
            return ret
        
        pipe = outpipe.split(":")
        for step in pipe:
            if step == "html":
                ret= htmlFormater(ret)
            elif step == "htmlinline":
                ret= htmlInlineFormater(ret)


            elif step == "html_bs_inline":
                ret= htmlBootstrapFormater(ret,inline=True)
            elif step == "html_bs":
                ret= htmlBootstrapFormater(ret,inline=False)


            elif step.startswith("save in "):
                dest = step.split(" ")[-1]
                savein(ret,dest)

            else:
                raise Exception("pipe step not found: %s"%step)

        return ret

