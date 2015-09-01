# -*- coding: utf-8 -*-
from __future__ import division, print_function, unicode_literals
import re
from . import manager, utils

Manager = manager.Manager

#===工具函数和类===#

def __d(**args):
    obj = utils.BaseClass()
    for k, v in args.items():
        obj.__setattr__(k, v)
    return obj

class __ListObj(list):
    def __str__(self):
        if hasattr(self, 'text'):
            return self.text.__str__()
        return list.__str__(self)
    def __repr__(self):
        if hasattr(self, 'text'):
            return self.text.__repr__()
        return list.__repr__(self)

class __StrObj(utils.TYPE_UNICODE):
    pass


def __help_tags_to(es, value, new_fun=lambda t:__ListObj()):
    oo = list()
    for index, tag in enumerate(value):
        o = new_fun(tag)
        o.start = tag.position
        o.length = tag.length
        o.end = tag.position + tag.length
        o.sdata = tag.sdata
        o.idata = tag.idata
        o.reserve = tag.reserve
        o.index = index
        oo.append(o)
    return oo

#===将manager返回的结果转化为python对象的函数===#

#token是一个list，token[x]是转换后字符串, token[x].orgin为原始字符串, token[x].index为下标x
def __to_token(es, value):
    oo = __help_tags_to(es, value, new_fun=lambda t:__StrObj(t.sdata))
    for index, o in enumerate(oo):
        o.orgin = es[o.start:o.end]
        o.index = index
    return oo

#sent是一个list，sent[x]为token, sent[x].text为原始句子, sent[x].index为下标x
def __to_sent(es, value):
    oo = __help_tags_to(es, value)
    for o in oo:
        o.extend(es.token[o.start:o.end])
        o.text = es[o[0].start:o[-1].end]
    return oo

#passage是一个list，passage[x]为sent, passage[x].text为原始段落
def __to_passage(es, value):
    oo = __help_tags_to(es, value)
    for o in oo:
        o.extend(es.sent[o.start:o.end])
        o.text = es[o[0][0].start:o[-1][-1].end]
    return oo

#spell是一个list，spell[x]为建议词list,spell[x][y]为第y个建议词, 
#spell[x].text为错误的token元素, spell[x].cc为可信度, spell[x].index为下标x
def __to_spell(es, value):
    oo = __help_tags_to(es, value)
    for o in oo:
        o.text = es.token[o.start]
        o.extend(o.sdata.split('|'))
        #confidence coefficient
        o.cc = o.idata
        o.sent_idx = len(es.sent) - 1
        o.pos_at_sent = len(es.sent[-1]) - 1
        for idx, s in enumerate(es.sent):
            if s.start > o.start:
                o.sent_idx = idx - 1
                o.pos_at_sent = o.start - es.sent[idx - 1].start
                break
    return oo

#family是一个list， 元素为每个token的family字符串
def __to_family(es, value):
    oo = __help_tags_to(es, value, new_fun=lambda t:__StrObj(t.sdata))
    return oo

#postag是一个list， 元素为每个token的词性
__TAGS = (".", ",", ":", "``", "''", "-LRB-", "-RRB-", "$", "#", ".$$.", "CC", "CD", "DT", "EX", "FW", "IN", "JJ", "JJR", "JJS", "LS",
          "MD", "NN", "NNP", "NNPS", "NNS", "PDT", "POS", "PRP", "PRP$", "RB", "RBR", "RBS", "RP", "SYM", "TO", "UH", "VB", "VBD", "VBG", "VBN",
         "VBP", "VBZ", "WDT", "WP", "WP$", "WRB")
def __to_postag(es, value):
    oo = __ListObj()
    oo.extend(map(lambda d:__TAGS[d], value[0].position))
    return oo

#lgram是一个list， 元素为每个token的链接数
def __to_lgram(es, value):
    oo = __ListObj()
    oo.extend(value[0].position)
    return oo

#jrgram是一个list， 元素为语法错误
#jrgram[x].text为错误的短语，jrgram[x].idata为所在的句子序号，jrgram[x].suggest为提示信息
#jrgram[x].start为错误短语的起始位置，jrgram[x].length为错误长度
def __to_jrgram(es, value):
    oo = __help_tags_to(es, value, new_fun=lambda t:__StrObj(' '.join(es.token[t.position: t.position + t.length])))
    for o in oo:
        o.suggest = o.sdata
        o.text = es[o.start: o.start + o.length + 1]
        o.sent_text = es.sent[o.idata]
        o.sent_idx = o.idata
    return oo

# jsyntax是一个list，其中有两种元素 reserve == 0: 是tregex pattern rule match 结果; reserve == 1: 是stanford parser dependencies结果
# 当reserve == 0时(表示tregex pattern rule match 结果)：
#   jsyntax[x].index: tregex pattern expression的index; 
#   jsyntax[x].idata: 当前所在sentence index
#   jsyntax[x].length: 在jsyntax[x].idata所示的句子中，第jsyntax[x].index个tregex pattern expression的match数
#   jsyntax[x].sdata: 当前tregex pattern rule的名称
#   jsyntax[x].reserve: 0
# 当reserve == 1时(表示句法树中存在的dependencies关系)：
#   一个dependencies关系的标准格式为: dependencies名称(主词-主词index, 从属词-从属词index), 例如: prep(a-1, b-12)
#   jsyntax[x].index: dependencies关系中，主词的index(在本句中的index)
#   jsyntax[x].length: dependencies关系中，从属词的index(在本句中的index)
#   jsyntax[x].sdata: dependencies名称
#   jsyntax[x].idata: 当前所在sentence index
#   jsyntax[x].reserve: 1
def __to_jsyntax(es, value):
    oo = __help_tags_to(es, value, new_fun=lambda t:__StrObj(' '.join(es.token[t.position: t.position + t.length])))
    for o in oo:
        o.is_dependence = o.reserve
        if o.is_dependence:
            o.gov_idx = o.index
            o.dep_idx = o.index
            o.dependence = o.sdata
        else:
            o.tregex_idx = o.index
            o.match_count = o.length
            o.tregex_name = o.sdata
        o.sent_text = es.sent[o.idata]
        o.sent_idx = o.idata
        o.node_cat = o.reserve
    return oo

#分析结果转化为python变量的函数
__value_map_funs = {
    'tToken':__to_token,
    'tSentence':__to_sent,
    'tPassage':__to_passage,
    'tSpelling':__to_spell,
    'tJRuleGrammar':__to_jrgram,
    'tWFamily':__to_family,
    'tPosTag':__to_postag,
    'tLinkGrammar':__to_lgram,
    'tJSyntax':__to_jsyntax,
}
__value_map_from = dict(map(lambda d:(d[1].__name__[len('__to'):], d[0]), __value_map_funs.items()))

supports = set(d[1:] for d in __value_map_from.keys())

__plaint_table_from = 'ＡＢＣＤＥＦＧＨＩＪＫＬＭＮＯＰＱＲＳＴＵＶＷＸＹＺａｂｃсｄｅｆｇｈｉｊｋｌｍｎｏｐｑｒｓｔｕｖｗｘｙｚ０１２３４５６７８９ⅠⅡⅢⅣⅤⅥⅦⅧⅨⅩⅪⅫàáâãäåæéêëèìíîïòóôõöùúûüç…，、．。？；！：“”‘’－—£￡'
__plaint_table_to = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabccdefghijklmnopqrstuvwxyz0123456789123456789000aaaaaaaeeeeiiiiooooouuuuc.,,..?;!:""\'\'--$$'
plaint_table = dict((ord(c), unicode(__plaint_table_to[idx])) for idx, c in enumerate(__plaint_table_from))
def plain_context(context):
    if not isinstance(context, utils.TYPE_UNICODE):
        context = context.decode('utf8')
    if not re.search('[^\r\n\t\x20-\x7f]', context):
        return context.encode('utf8')
    context = context.translate(plaint_table)
    context = re.sub('[^\r\n\t\x20-\x7f]', ' ', context)
    return context.encode('utf8')

def process(context, **args):
    """
    分析一个文本，返回一个Essay对象
    context     原文
    args        为需返回的结果和传递的分析参数，
                1. 返回结果用"_"前缀，例如:_token=1表示需要token
                                        _passage=1表示需要分段
                   程序会自动处理依赖关系，写成"process(xx, _passage=1)"和"process(xx, _token=1,_sent=1,_passage=1)"是一样的
                   支持的参数见__value_map_funs变量，后面的值去掉"__to"前缀即是。
                2. 分析参数，如fSpellingCorrectorParamLamda=1.0
    例子：1. process('This is a test.', _passage=1) 等价于process('This is a test.', _token=1,_sent=1,_passage=1)
          2. process('This is a test.', _spell=1, fSpellingParamLamda=0.1, fSpellingParamAlpha=0.05) 
    """
    class Essay(utils.TYPE_UNICODE):
        pass
    needs = list()
    params = dict()
    for k, v in args.items():
        if k.startswith('_'):
            if not __value_map_from.has_key(k):
                v and needs.append(k[1:])
                continue
            v and needs.append(__value_map_from[k])
        elif v != None:
            params[k] = v
    rs = Manager.process_task(' '.join(needs), plain_context(context), **params)
    if isinstance(context, utils.TYPE_UNICODE) and type(context) != utils.TYPE_UNICODE:
        es = context
    else:
        es = Essay(context)
    for k, v in rs:
        if not __value_map_funs.has_key(k):
            es.__setattr__(k, v)
            continue
        fun = __value_map_funs[k]
        es.__setattr__(fun.__name__[len('__to_'):], fun(es, v))
    return es


#统计基类#
class AbstractStat(object):
    #输入参数
    inputs = set()
    #输出参数
    outputs = dict()
    #输出参数的中文解释
    def process(self, es, **args):
        raise NotImplementedError

#统计处理类#
class StatProcess(object):
    #输入参数为list,元素为AbstractStat的继承类的实例
    def __init__(self, *list_of_derived_stat):
        self.__needs = set()
        self.__stats = list()
        self.outputs = dict()
        #
        old = list_of_derived_stat
        list_of_derived_stat = list()
        for an in old:
            if isinstance(an, AbstractStat):
                list_of_derived_stat.append(an)
            else:
                list_of_derived_stat.extend(an)
        #
        output_to_an = dict()
        for an in list_of_derived_stat:
            for o in an.outputs:
                output_to_an[o] = an
            self.outputs.update(an.outputs)
        for an in list_of_derived_stat:
            _inputs = set()
            for i in an.inputs:
                if i in supports:
                    self.__needs.add('_' + i)
                elif i in output_to_an:
                    _inputs.add(output_to_an[i])
            an._inputs = _inputs
        __analysers_tmp = set(list_of_derived_stat)
        while __analysers_tmp:
            emp = set()
            for an in __analysers_tmp:
                if not an._inputs:
                    emp.add(an)
            if not emp:
                raise AssertionError('存在循环依赖项')
            __analysers_tmp -= emp
            for an in __analysers_tmp:
                an._inputs -= emp
            self.__stats.extend(emp)
    #
    def process(self, context, **args):
        global process
        for need in self.__needs:
            args[need] = 1
        es = process(context, **args)
        for an in self.__stats:
            an.process(es, **args)
        return es

if __name__ == '__main__':

    #测试配置
    do_process_tokenizer = True
    do_process_spelling = False
    do_process_linkgrammar = False
    do_process_wordclassifier = False
    do_process_jrgcheck = False
    
    if do_process_jrgcheck:
        test_case = 'The book are good. I can know say something more. What jar is this suppose to be comming from? I can know say something more.'
        es = process(test_case, _jrgram=1)
        print(es.token)
        print(es.sent)
        print(es.jrgram)
        print()
    
    if do_process_tokenizer:
        test_case = 'Thiiis is a test. This is a test, too. She said:"Hello,World!"  \n\n\n This is the seconde passage .  \n  \n   And the last one sentence.'
        es = process(test_case, _passage=1, _postag=1)
        print(es.token)
        print(' '.join(es.token))
        print(es.sent)
        print(es.passage)
        print(es.postag)
        print()
    
    if do_process_spelling:
        test_case = 'Thiiis is a test. This is a test, too. She said:"Hello,World!"'
        es = process(test_case, _spell=1)
        print(es.token)
        print(es.sent)
        print(es.spell)
        print()
    
    if do_process_linkgrammar:
        test_case = "use linkgrammar, we can tell you if a sentence is correct. For example, this sentence itself is a correct sentence. However, hellow world is a wrong one."
        es = process(test_case, _lgram=1)
        print(es.token)
        print(es.sent)
        print(es.lgram)
        print()
    
    if do_process_wordclassifier:
        test_case = "It seems many Chinese are stuck between their common sense and the unspoken rules of ganbei culture."
        es = process(test_case, _family=1)
        print(es.family)
        print()
