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
    re_h=re.compile('</?[^(img)(br)(iframe)][^>]*>')#HTML标签
    s=re_h.sub('',s) #去掉HTML 标签

    #去掉多余的空行
    blank_line=re.compile('\n+')
    s=blank_line.sub('<br/>',s)

    re_br=re.compile('(<br\s*?/?>\s*)+')#处理换行
    s=re_br.sub('<br/>',s)#将br转换为换行

    re_space = re.compile(r'　+')
    s=re_space.sub(' ',s)

    html_parser = HTMLParser()
    s=html_parser.unescape(s)

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
    str =u'''<iframe src="432432"></iframe>432432432'''
    print(filter_tags2(str))