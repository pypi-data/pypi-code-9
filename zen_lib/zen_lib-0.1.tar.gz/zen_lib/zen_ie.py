# -*- coding: gbk -*-
from win32com.client import DispatchEx
import time
"""
import sys
sys.path.append("D:\\icbc\\icbc_coding\\")
import zen_ie
20150412 重构

"""


    
def getIE(url="www.baidu.com"):
    global ie
    ie = None
    ShellWindowsCLSID = '{9BA05972-F6A8-11CF-A442-00A0C90A8F39}'
    ies = DispatchEx(ShellWindowsCLSID)
    for i in ies:
        if i.LocationURL.count(url) > 0:
            print "get ie"
            ie = i
    if ie == None:
        ie = DispatchEx('InternetExplorer.Application')
        ie.Visible = 1
        ie.Navigate(url)
        print "new ie"
    return ie
def searchIE(url_keys=["http://exam/wis18/usermain/paper/userpaper.answeruserpapercurr.flow?sid=", "http://exam/wis18/usermain/main/paper.builduserpapercurr.flow?sid="]):
    global ie
    ie = None
    ShellWindowsCLSID = '{9BA05972-F6A8-11CF-A442-00A0C90A8F39}'
    apps = DispatchEx(ShellWindowsCLSID)
    for i in apps:
        if type(url_keys) == type("") or type(url_keys) == type(u""):
            for j in url_keys:
                if i.LocationURL.count(j) > 0:
                    print "IE match,key=" + url_keys
                    ie = i  
        elif type(url_keys) == type([]):
            for j in url_keys:
                if i.LocationURL.count(j) > 0:
                    print "IE match,key=" + j
                    ie = i            
    apps = None
    if ie == None:
        time.sleep(0.7)
        searchIE(url_keys)
    return ie
def waitIE():
    global ie
    while ie.Busy:
        time.sleep(0.25)

def getElement(doc, tag, nodeattr, nodeval):
    """
    <input name="wd" class="s_ipt" id="kw" maxlength="100" value="" autocomplete="off">


百度测试
    getElement("input","id","kw").value=str(time.time())
    getElement("input","id","su").click()
    """
    result = []
    waitIE()
    body = doc.body
    for node in body.getElementsByTagName(tag):
        if str(node.getAttribute(nodeattr)) == nodeval:
            result.append(node)
    frames = doc.frames
    if frames.length > 0:
        for i in range (frames.length):
            doc_in = frames[i].Document
            tmp = getElement(doc_in, tag, nodeattr, nodeval)
            if not tmp == []:
                for e in tmp:
                    result.append(e) 
    
    return result




def GetBody():
    global ie
    return ie.Document.body
def GetNodes(parentNode, tag):
    childNodes = []
    for childNode in parentNode.getElementsByTagName(tag):
        childNodes.append(childNode)
    return childNodes
def NodeByAttr(Nodes, nodeattr, nodeval):
    for node in Nodes:
        if str(node.getAttribute(nodeattr)) == nodeval:
            return node
    return None
def SetNode(node, val):
    node.innerHTML = val


# #ie=getIE("R:\\12.html")
# #doc=ie.Document
# #body=doc.body
# #frames=doc.frames
# #frame=frames[0]
# #getElement("input","name","fpdm").value=str(time.time())
# getElement("input","id","kw1").value=str(time.time())
# getElement("input","id","su1").click()
# #input_ids=GetNodes(body,"input")
# #input_id_email=NodeByAttr(input_ids,"id","kw1")
# #input_id_email.value="123123123123"
# #input_id_login=NodeByAttr(input_ids,"id","su1")
# #input_id_login.click()
