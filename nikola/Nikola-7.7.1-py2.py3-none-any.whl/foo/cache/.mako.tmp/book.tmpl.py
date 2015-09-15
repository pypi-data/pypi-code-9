# -*- coding:utf-8 -*-
from mako import runtime, filters, cache
UNDEFINED = runtime.UNDEFINED
__M_dict_builtin = dict
__M_locals_builtin = locals
_magic_number = 10
_modified_time = 1441941103.823588
_enable_loop = True
_template_filename = u'templates/book.tmpl'
_template_uri = u'book.tmpl'
_source_encoding = 'utf-8'
_exports = [u'content', u'extra_head']


def _mako_get_namespace(context, name):
    try:
        return context.namespaces[(__name__, name)]
    except KeyError:
        _mako_generate_namespaces(context)
        return context.namespaces[(__name__, name)]
def _mako_generate_namespaces(context):
    ns = runtime.TemplateNamespace(u'pheader', context._clean_inheritance_tokens(), templateuri=u'post_header.tmpl', callables=None,  calling_uri=_template_uri)
    context.namespaces[(__name__, u'pheader')] = ns

    ns = runtime.TemplateNamespace(u'comments', context._clean_inheritance_tokens(), templateuri=u'comments_helper.tmpl', callables=None,  calling_uri=_template_uri)
    context.namespaces[(__name__, u'comments')] = ns

    ns = runtime.TemplateNamespace(u'helper', context._clean_inheritance_tokens(), templateuri=u'post_helper.tmpl', callables=None,  calling_uri=_template_uri)
    context.namespaces[(__name__, u'helper')] = ns

def _mako_inherit(template, context):
    _mako_generate_namespaces(context)
    return runtime._inherit_from(context, u'post.tmpl', _template_uri)
def render_body(context,**pageargs):
    __M_caller = context.caller_stack._push_frame()
    try:
        __M_locals = __M_dict_builtin(pageargs=pageargs)
        pheader = _mako_get_namespace(context, 'pheader')
        def extra_head():
            return render_extra_head(context._locals(__M_locals))
        helper = _mako_get_namespace(context, 'helper')
        parent = context.get('parent', UNDEFINED)
        messages = context.get('messages', UNDEFINED)
        comments = _mako_get_namespace(context, 'comments')
        def content():
            return render_content(context._locals(__M_locals))
        site_has_comments = context.get('site_has_comments', UNDEFINED)
        enable_comments = context.get('enable_comments', UNDEFINED)
        post = context.get('post', UNDEFINED)
        __M_writer = context.writer()
        __M_writer(u'\n')
        __M_writer(u'\n')
        __M_writer(u'\n')
        __M_writer(u'\n\n')
        if 'parent' not in context._data or not hasattr(context._data['parent'], 'extra_head'):
            context['self'].extra_head(**pageargs)
        

        __M_writer(u'\n\n')
        if 'parent' not in context._data or not hasattr(context._data['parent'], 'content'):
            context['self'].content(**pageargs)
        

        __M_writer(u'\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_content(context,**pageargs):
    __M_caller = context.caller_stack._push_frame()
    try:
        pheader = _mako_get_namespace(context, 'pheader')
        helper = _mako_get_namespace(context, 'helper')
        messages = context.get('messages', UNDEFINED)
        comments = _mako_get_namespace(context, 'comments')
        def content():
            return render_content(context)
        site_has_comments = context.get('site_has_comments', UNDEFINED)
        enable_comments = context.get('enable_comments', UNDEFINED)
        post = context.get('post', UNDEFINED)
        __M_writer = context.writer()
        __M_writer(u'\n<article class="storypage" itemscope="itemscope" itemtype="http://schema.org/Article">\n    <div class="frame">\n    <div class="scrolling-cont" id="scrolling-cont" name="scrolling-cont">\n    <div class="e-content entry-content chapter" itemprop="articleBody text">\n    ')
        __M_writer(unicode(pheader.html_title()))
        __M_writer(u'\n    ')
        __M_writer(unicode(post.text()))
        __M_writer(u'\n    </div>\n    </div>\n    </div>\n')
        if site_has_comments and enable_comments and not post.meta('nocomments'):
            __M_writer(u'        <section class="comments">\n        <h2>')
            __M_writer(unicode(messages("Comments")))
            __M_writer(u'</h2>\n        ')
            __M_writer(unicode(comments.comment_form(post.permalink(absolute=True), post.title(), post.base_path)))
            __M_writer(u'\n        </section>\n')
        __M_writer(u'    ')
        __M_writer(unicode(helper.mathjax_script(post)))
        __M_writer(u"\n    <script>\n    $('#scrolling-cont').flowtype({\n        minimum   : 500,\n        maximum   : 1200,\n        minFont   : 20,\n        maxFont   : 40,\n        fontRatio : 50\n    });\n    $(document).ready(function() {\n        var elem = $('#scrolling-cont');\n        elem.click(function(event) {\n            var x1 = elem.position().left;\n            var pw = elem.width() + 20;\n            var x2 = event.pageX;\n            if (x2-x1 < pw/2) {\n                pw = -pw;\n            }\n            elem.animate({scrollLeft: '+='+pw}, 500)\n        });\n    });\n    </script>\n</article>\n\n")
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_extra_head(context,**pageargs):
    __M_caller = context.caller_stack._push_frame()
    try:
        def extra_head():
            return render_extra_head(context)
        parent = context.get('parent', UNDEFINED)
        __M_writer = context.writer()
        __M_writer(u'\n    ')
        __M_writer(unicode(parent.extra_head()))
        __M_writer(u'\n    <script src="/assets/js/jquery.min.js"></script>\n    <script src="//cdnjs.cloudflare.com/ajax/libs/Flowtype.js/1.1.0/flowtype.min.js"></script>\n    <link href=\'https://fonts.googleapis.com/css?family=Gentium+Book+Basic\' rel=\'stylesheet\' type=\'text/css\'>\n    <link href=\'https://fonts.googleapis.com/css?family=Rye\' rel=\'stylesheet\' type=\'text/css\'>\n<style>\n        p {\n            text-align: justify;\n        }\n .chapter {\n    width: 100%;\n    padding: 10px 10px;\n    -webkit-column-gap: 40px;\n    -webkit-column-width: 400px;\n    -webkit-column-count: 2;\n    -webkit-column-rule: 1px solid #ddd;\n    height: 800px;\n    font-family: \'Gentium Book Basic\', serif;\n    font-color: #2d2e2e;\n    }\n\n    div.frame {\n        overflow: hidden;\n        padding: 0;\n        margin: 0;\n    }\n    div.scrolling-cont {\n    overflow-x: scroll;\n    padding: 0;\n    margin: 0;\n    }\n\n    h1, h2, h3, h4 {\n        text-align: center;\n        width: 100%;\n        font-family: \'Rye\', cursive;\n        font-size: 120%;\n    }\n\n    h1 {\n        font-size: 150%;\n    }\n\n    .figure2 {\n    height: 40%;\n    padding-bottom: 20%;\n    }\n    .figure1 {\n    height: 800px;\n    padding:  0;\n    margin: 0;\n    }\n\n    .illus1, .front {\n        margin-left: auto;\n        margin-right: auto;\n        max-height: 500px;\n    }\n    .illus1 {\n        height: 700px;\n        width: auto;\n        margin: 0;\n    }\n\n    div.topic {\n        margin: 0;\n    }\n    </style>\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


"""
__M_BEGIN_METADATA
{"source_encoding": "utf-8", "line_map": {"22": 3, "25": 4, "28": 2, "34": 0, "51": 2, "52": 3, "53": 4, "54": 5, "59": 76, "64": 118, "70": 78, "83": 78, "84": 83, "85": 83, "86": 84, "87": 84, "88": 88, "89": 89, "90": 90, "91": 90, "92": 91, "93": 91, "94": 94, "95": 94, "96": 94, "102": 7, "109": 7, "110": 8, "111": 8, "117": 111}, "uri": "book.tmpl", "filename": "templates/book.tmpl"}
__M_END_METADATA
"""
