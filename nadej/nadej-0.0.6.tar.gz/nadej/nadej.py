
import os
from StringIO import StringIO
from  htmlout import htmlInlineFormater,htmlBootstrapFormater,htmlFormater

import json


def savein(data,dest):
    """

    save data in html
    """
    if os.path.isabs(dest) :
        return
    
    
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

    def json(self,text=""):
        dic = {"type":"code",
                "format":"json",
                "text":text}
        if isinstance(text,dict):
            dic = {"type":"code",
                "format":"json",
                "text":json.dumps(text)}
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


    def plot(self,data=""):
        """
        """
        import pandas as pd

        if isinstance(data,pd.DataFrame):
            import matplotlib
            #matplotlib.use('Agg')
            import matplotlib.pyplot as plt
            plt.figure()
            for col in data:
                plt.plot(data.index,data[col],label=col)

            plt.legend()

            bufferIMG = StringIO()
            plt.savefig(bufferIMG)
            # out put as png
            from base64 import b64encode,b64decode
            buffer64 = b64encode(bufferIMG.getvalue())

            self.png(buffer64)

        else:
            raise Exception("not supported yet")
    def split(self,act="1"):
        """
        If act is 

        * vsplit: it starts a vertical Split
        * end: it ends the last opened element

        """
        
        if act == "vsplit":
            dic = {"type":"vsplit",
                    "count":1}
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
        previousCount = self.state[-1]["count"]
        self.state[-1]["count"] = previousCount+1
        
        dic = {"type":"then",}
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

