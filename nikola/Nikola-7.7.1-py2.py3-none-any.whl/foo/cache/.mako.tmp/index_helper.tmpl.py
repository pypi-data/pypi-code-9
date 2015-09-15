# -*- coding:utf-8 -*-
from mako import runtime, filters, cache
UNDEFINED = runtime.UNDEFINED
__M_dict_builtin = dict
__M_locals_builtin = locals
_magic_number = 10
_modified_time = 1441941103.793643
_enable_loop = True
_template_filename = u'/home/ralsina/Desktop/proyectos/nikola/master/nikola/data/themes/base/templates/index_helper.tmpl'
_template_uri = u'index_helper.tmpl'
_source_encoding = 'utf-8'
_exports = ['mathjax_script', 'html_pager']


def render_body(context,**pageargs):
    __M_caller = context.caller_stack._push_frame()
    try:
        __M_locals = __M_dict_builtin(pageargs=pageargs)
        __M_writer = context.writer()
        __M_writer(u'\n\n')
        __M_writer(u'\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_mathjax_script(context,posts):
    __M_caller = context.caller_stack._push_frame()
    try:
        any = context.get('any', UNDEFINED)
        use_katex = context.get('use_katex', UNDEFINED)
        __M_writer = context.writer()
        __M_writer(u'\n')
        if any(post.is_mathjax for post in posts):
            if use_katex:
                __M_writer(u'            <script src="//cdnjs.cloudflare.com/ajax/libs/KaTeX/0.3.0/katex.min.js"></script>\n            <script src="//cdnjs.cloudflare.com/ajax/libs/KaTeX/0.3.0/contrib/auto-render.min.js"></script>\n            <script>\n                renderMathInElement(document.body);\n            </script>\n')
            else:
                __M_writer(u'            <script type="text/javascript" src="//cdn.mathjax.org/mathjax/latest/MathJax.js?config=TeX-AMS-MML_HTMLorMML"> </script>\n            <script type="text/x-mathjax-config">\n            MathJax.Hub.Config({tex2jax: {inlineMath: [[\'$latex \',\'$\'], [\'\\\\(\',\'\\\\)\']]}});\n            </script>\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_html_pager(context):
    __M_caller = context.caller_stack._push_frame()
    try:
        prevlink = context.get('prevlink', UNDEFINED)
        messages = context.get('messages', UNDEFINED)
        nextlink = context.get('nextlink', UNDEFINED)
        __M_writer = context.writer()
        __M_writer(u'\n')
        if prevlink or nextlink:
            __M_writer(u'        <nav class="postindexpager">\n        <ul class="pager">\n')
            if prevlink:
                __M_writer(u'            <li class="previous">\n                <a href="')
                __M_writer(unicode(prevlink))
                __M_writer(u'" rel="prev">')
                __M_writer(unicode(messages("Newer posts")))
                __M_writer(u'</a>\n            </li>\n')
            if nextlink:
                __M_writer(u'            <li class="next">\n                <a href="')
                __M_writer(unicode(nextlink))
                __M_writer(u'" rel="next">')
                __M_writer(unicode(messages("Older posts")))
                __M_writer(u'</a>\n            </li>\n')
            __M_writer(u'        </ul>\n        </nav>\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


"""
__M_BEGIN_METADATA
{"source_encoding": "utf-8", "line_map": {"15": 0, "20": 19, "21": 36, "27": 21, "33": 21, "34": 22, "35": 23, "36": 24, "37": 29, "38": 30, "44": 2, "51": 2, "52": 3, "53": 4, "54": 6, "55": 7, "56": 8, "57": 8, "58": 8, "59": 8, "60": 11, "61": 12, "62": 13, "63": 13, "64": 13, "65": 13, "66": 16, "72": 66}, "uri": "index_helper.tmpl", "filename": "/home/ralsina/Desktop/proyectos/nikola/master/nikola/data/themes/base/templates/index_helper.tmpl"}
__M_END_METADATA
"""
