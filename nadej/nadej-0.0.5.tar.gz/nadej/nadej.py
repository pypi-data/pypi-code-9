
import os
from StringIO import StringIO
from  htmlout import htmlInlineFormater,htmlBootstrapFormater,htmlFormater


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
            matplotlib.use('Agg')
            import matplotlib.pyplot as plt
            plt.plot(data)
            
            plt.legend(data.columns)

            bufferIMG = StringIO()
            plt.savefig(bufferIMG)
            from base64 import b64encode,b64decode

            buffer64 = b64encode(bufferIMG.getvalue())

            self.png(buffer64)

        else:
            raise Exception("not supported yet")

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
            elif step == "html_bs":
                
                
                ret= htmlBootstrapFormater(ret)
            elif step.startswith("save in "):
                dest = step.split(" ")[-1]
                savein(ret,dest)

            else:
                raise Exception("pipe step not found: %s"%step)

        return ret

