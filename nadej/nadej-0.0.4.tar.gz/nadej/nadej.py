


class ClientAPI(object):

    dataList = []

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

    def collect(self):
        """
        """
        ret = self.dataList
        self.dataList=[]
        return ret
    def png(self,data):
        """
        """
        dic = {"type":"img",
               "form":"png",
               "data":data}
        self.dataList.append(dic)

