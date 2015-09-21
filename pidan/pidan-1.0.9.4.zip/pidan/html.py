# -*- coding: utf-8 -*-
#html代码相关的函数
import re
from HTMLParser import HTMLParser

def html2js(content,format='string'):
    '''将html代码转换成js代码'''
    import re

    tab = '    '
    format = 'array'

    html = content\
           .replace('\r', '')\
           .replace('\n', '')\
           .replace('"', r'\"')\
           .replace('\'', r'\'')

    return html


def filter_tags(htmlstr):
    #先过滤CDATA
    re_cdata=re.compile('//<!\[CDATA\[[^>]*//\]\]>',re.I) #匹配CDATA
    re_script=re.compile('<\s*script[^>]*>[^<]*<\s*/\s*script\s*>',re.I)#Script
    re_style=re.compile('<\s*style[^>]*>[^<]*<\s*/\s*style\s*>',re.I)#style
    re_br=re.compile('<br\s*?/?>')#处理换行
    re_h=re.compile('</?[\w+^(img)][^>]*>')#HTML标签
    re_comment=re.compile('<!--[^>]*-->')#HTML注释
    s=re_cdata.sub('',htmlstr)#去掉CDATA
    s=re_script.sub('',s) #去掉SCRIPT
    s=re_style.sub('',s)#去掉style
    s=re_br.sub('\n',s)#将br转换为换行
    s=re_h.sub('',s) #去掉HTML 标签
    s=re_comment.sub('',s)#去掉HTML注释
    #去掉多余的空行
    blank_line=re.compile('\n+')
    s=blank_line.sub('\n',s)
    return s


def filter_tags2(htmlstr):
    '''智能过滤html标签，但保留图片和换行'''
    s=htmlstr

    #危险内容，从标签到内容全部过滤
    re_cdata=re.compile('//<!\[CDATA\[[^>]*//\]\]>',re.I) #匹配CDATA
    s=re_cdata.sub('',s)#去掉CDATA

    re_script=re.compile('<\s*script[^>]*>[^<]*<\s*/\s*script\s*>',re.I)#Script
    s=re_script.sub('',s) #去掉SCRIPT

    re_style=re.compile('<\s*style[^>]*>[^<]*<\s*/\s*style\s*>',re.I)#style
    s=re_style.sub('',s)#去掉style

    re_comment=re.compile('<!--[^>]*-->')#HTML注释
    s=re_comment.sub('',s)#去掉HTML注释

    #非危险内容，过滤标签，但保留内容
    re_h=re.compile('</?[^(img)(br)][^>]*>')#HTML标签
    s=re_h.sub('',s) #去掉HTML 标签

    #去掉多余的空行
    blank_line=re.compile('\n+')
    s=blank_line.sub('<br/>',s)

    re_br=re.compile('(<br\s*?/?>\s*)+')#处理换行
    s=re_br.sub('<br/>',s)#将br转换为换行



    return s

def strip_tags(html):
    '''删除掉所有的html标签'''
    html = html.strip()
    html = html.strip("\n")
    result = []
    parse = HTMLParser()
    parse.handle_data = result.append
    parse.feed(html)
    parse.close()
    return "".join(result)

def get_image_urls(content):
    '''得到html代码中的所有图片地址'''
    str=r'''<img\b[^<>]*?\bsrc[\s\t\r\n]*=[\s\t\r\n]*["']?[\s\t\r\n]*([^\s\t\r\n"'<>]*)[^<>]*?/?[\s\t\r\n]*>'''
    #str='src="(.*?)\.jpg"'
    reObj=re.compile(str,re.IGNORECASE)
    allMatch=reObj.findall(content)
    if allMatch:
        return allMatch
    else:
        return []


if __name__ == '__main__':
    str =u'''<div style="width:92%;margin-right:auto;margin-left:auto;margin-bottom:auto;"><p style="margin: 21px 0px; line-height: 1.5; color: rgb(0, 0, 0); font-size: 16px;"> <font face="sans-serif"><img alt="" src="http://bdapp.bandao.cn/bandao/uploads/allimg/150913/14-1509130S501342.jpg" style="border: 0px; max-width:100%;" /></font><br /> <span style="color:#a9a9a9;"><span style="font-family: 宋体; font-size: 17px; line-height: 25.5px;">省委常委、市委书记李群和世界休闲组织主席罗杰</span><span style="font-size: 17px; line-height: 25.5px;"><font face="sans-serif">&middot;</font></span><span style="font-family: 宋体; font-size: 17px; line-height: 25.5px;">科尔斯一起观看休体大会开幕式。</span></span><br /> <br /> <img alt="" src="http://bdapp.bandao.cn/bandao/uploads/allimg/150913/14-1509130U344334.jpg" style="border: 0px; max-width:100%;" /><br /> <span style="color:#a9a9a9;">休体大会开幕式现场。</span><br /> <br /> 　　<span style="font-family: 宋体; font-size: 17px; line-height: 25.5px;">历经三年的建设和期待，</span><span style="font-family: sans-serif; font-size: 17px; line-height: 25.5px;">9</span><span style="font-family: 宋体; font-size: 17px; line-height: 25.5px;">月</span><span style="font-family: sans-serif; font-size: 17px; line-height: 25.5px;">12</span><span style="font-family: 宋体; font-size: 17px; line-height: 25.5px;">日，美丽热情的岛城又迎来一场国际赛事</span><span style="font-family: sans-serif; font-size: 17px; line-height: 25.5px;">&mdash;&mdash;2015</span><span style="font-family: 宋体; font-size: 17px; line-height: 25.5px;">世界休闲体育大会。省委常委、市委书记李群，市委副书记、市长张新起，在休闲大会举办地莱西，会见了世界休闲组织罗杰</span><span style="font-family: sans-serif; font-size: 17px; line-height: 25.5px;">&middot;</span><span style="font-family: 宋体; font-size: 17px; line-height: 25.5px;">科尔斯主席一行。</span></p> <p style="margin: 21px 0px; line-height: 1.5; color: rgb(0, 0, 0); font-size: 16px;"> <span style="font-family: sans-serif; font-size: 17px; line-height: 25.5px;">　　</span><span style="font-family: 宋体; font-size: 17px; line-height: 25.5px;">李群用流利的英语对客人说：&ldquo;今天青岛的天气特别给面子，正在下着的漂泼大雨，见到贵宾来后立即转晴，可见青岛的雨多么有&lsquo;科技含量&rsquo;&rdquo;。李群书记幽默的开场让罗杰</span><span style="font-size: 17px; line-height: 25.5px;"><font face="sans-serif">&middot;</font></span><span style="font-family: 宋体; font-size: 17px; line-height: 25.5px;">科尔斯倍感轻松，没有语言的障碍，瞬间拉近了两个人的距离，在一片笑声中，双方开启了愉快的会谈。</span></p> <p style="margin: 21px 0px; line-height: 1.5; color: rgb(0, 0, 0); font-family: sans-serif; font-size: 16px;"> <span style="font-size: 17px; line-height: 25.5px;">　　</span><span style="font-size: 17px; line-height: 25.5px; font-family: 宋体;">李群首先代表市委市政府对世界休闲组织罗杰</span><span style="font-size: 17px; line-height: 25.5px;">&middot;</span><span style="font-size: 17px; line-height: 25.5px; font-family: 宋体;">科尔斯主席一行的到来表示热烈欢迎</span><span style="font-size: 17px; line-height: 25.5px; font-family: 宋体;">。他说，休闲和体育的融合彰显了体育本质，让体育走进自然、走进百姓，代表了体育发展的方向。李群表示：&ldquo;世界休闲组织必会为希望助力，青岛将大力发展、普及休闲体育运动，共同为人类全面健康发展作出努力。&rdquo;</span></p> <p style="margin: 21px 0px; line-height: 1.5; color: rgb(0, 0, 0); font-size: 16px;"> <span style="font-family: sans-serif; font-size: 17px; line-height: 25.5px;">　　&quot;</span><span style="font-family: 宋体; font-size: 17px; line-height: 25.5px;">我太赞成您的观点了，您为我们世界休闲组织的性质进行了深刻诠释，我要好好改改我原定的讲话。</span><span style="font-family: sans-serif; font-size: 17px; line-height: 25.5px;">&quot;</span><span style="font-family: 宋体; font-size: 17px; line-height: 25.5px;">罗杰</span><span style="font-size: 17px; line-height: 25.5px;"><font face="sans-serif">&middot;</font></span><span style="font-family: 宋体; font-size: 17px; line-height: 25.5px;">科尔斯笑着说，他之前参观了各种场馆设施感觉都很棒，很高兴能在青岛举办这次大会，希望未来双方有着更多的合作。</span></p> <p style="margin: 21px 0px; line-height: 1.5; color: rgb(0, 0, 0); font-family: sans-serif; font-size: 16px;"> <span style="font-size: 17px; line-height: 25.5px;">　　</span><span style="font-size: 17px; line-height: 25.5px; font-family: 宋体;">据了解，世界休闲体育大会每五年举办一届，首届世界休闲体育大会于</span><span style="font-size: 17px; line-height: 25.5px;">2010</span><span style="font-size: 17px; line-height: 25.5px; font-family: 宋体;">年在韩国春川市举行，本次在青岛莱西举办的正是第二届。</span></p> </div>'''
    print(filter_tags2(str))