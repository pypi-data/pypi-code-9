# -*- coding:utf-8 -*-
from mako import runtime, filters, cache
UNDEFINED = runtime.UNDEFINED
__M_dict_builtin = dict
__M_locals_builtin = locals
_magic_number = 10
_modified_time = 1441941103.83978
_enable_loop = True
_template_filename = u'/home/ralsina/Desktop/proyectos/nikola/master/nikola/data/themes/base/templates/post_helper.tmpl'
_template_uri = u'post_helper.tmpl'
_source_encoding = 'utf-8'
_exports = ['html_tags', 'html_pager', 'twitter_card_information', 'meta_translations', 'mathjax_script', 'open_graph_metadata']


def render_body(context,**pageargs):
    __M_caller = context.caller_stack._push_frame()
    try:
        __M_locals = __M_dict_builtin(pageargs=pageargs)
        __M_writer = context.writer()
        __M_writer(u'\n')
        __M_writer(u'\n\n')
        __M_writer(u'\n\n')
        __M_writer(u'\n\n')
        __M_writer(u'\n\n')
        __M_writer(u'\n\n')
        __M_writer(u'\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_html_tags(context,post):
    __M_caller = context.caller_stack._push_frame()
    try:
        _link = context.get('_link', UNDEFINED)
        hidden_tags = context.get('hidden_tags', UNDEFINED)
        __M_writer = context.writer()
        __M_writer(u'\n')
        if post.tags:
            __M_writer(u'        <ul itemprop="keywords" class="tags">\n')
            for tag in post.tags:
                if tag not in hidden_tags:
                    __M_writer(u'            <li><a class="tag p-category" href="')
                    __M_writer(unicode(_link('tag', tag)))
                    __M_writer(u'" rel="tag">')
                    __M_writer(unicode(tag))
                    __M_writer(u'</a></li>\n')
            __M_writer(u'        </ul>\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_html_pager(context,post):
    __M_caller = context.caller_stack._push_frame()
    try:
        messages = context.get('messages', UNDEFINED)
        __M_writer = context.writer()
        __M_writer(u'\n')
        if post.prev_post or post.next_post:
            __M_writer(u'        <ul class="pager hidden-print">\n')
            if post.prev_post:
                __M_writer(u'            <li class="previous">\n                <a href="')
                __M_writer(unicode(post.prev_post.permalink()))
                __M_writer(u'" rel="prev" title="')
                __M_writer(filters.html_escape(unicode(post.prev_post.title())))
                __M_writer(u'">')
                __M_writer(unicode(messages("Previous post")))
                __M_writer(u'</a>\n            </li>\n')
            if post.next_post:
                __M_writer(u'            <li class="next">\n                <a href="')
                __M_writer(unicode(post.next_post.permalink()))
                __M_writer(u'" rel="next" title="')
                __M_writer(filters.html_escape(unicode(post.next_post.title())))
                __M_writer(u'">')
                __M_writer(unicode(messages("Next post")))
                __M_writer(u'</a>\n            </li>\n')
            __M_writer(u'        </ul>\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_twitter_card_information(context,post):
    __M_caller = context.caller_stack._push_frame()
    try:
        twitter_card = context.get('twitter_card', UNDEFINED)
        __M_writer = context.writer()
        __M_writer(u'\n')
        if twitter_card and twitter_card['use_twitter_cards']:
            __M_writer(u'    <meta name="twitter:card" content="')
            __M_writer(filters.html_escape(unicode(twitter_card.get('card', 'summary'))))
            __M_writer(u'">\n')
            if 'site:id' in twitter_card:
                __M_writer(u'    <meta name="twitter:site:id" content="')
                __M_writer(unicode(twitter_card['site:id']))
                __M_writer(u'">\n')
            elif 'site' in twitter_card:
                __M_writer(u'    <meta name="twitter:site" content="')
                __M_writer(unicode(twitter_card['site']))
                __M_writer(u'">\n')
            if 'creator:id' in twitter_card:
                __M_writer(u'    <meta name="twitter:creator:id" content="')
                __M_writer(unicode(twitter_card['creator:id']))
                __M_writer(u'">\n')
            elif 'creator' in twitter_card:
                __M_writer(u'    <meta name="twitter:creator" content="')
                __M_writer(unicode(twitter_card['creator']))
                __M_writer(u'">\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_meta_translations(context,post):
    __M_caller = context.caller_stack._push_frame()
    try:
        lang = context.get('lang', UNDEFINED)
        sorted = context.get('sorted', UNDEFINED)
        translations = context.get('translations', UNDEFINED)
        len = context.get('len', UNDEFINED)
        __M_writer = context.writer()
        __M_writer(u'\n')
        if len(translations) > 1:
            for langname in sorted(translations):
                if langname != lang and post.is_translation_available(langname):
                    __M_writer(u'                <link rel="alternate" hreflang="')
                    __M_writer(unicode(langname))
                    __M_writer(u'" href="')
                    __M_writer(unicode(post.permalink(langname)))
                    __M_writer(u'">\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_mathjax_script(context,post):
    __M_caller = context.caller_stack._push_frame()
    try:
        use_katex = context.get('use_katex', UNDEFINED)
        __M_writer = context.writer()
        __M_writer(u'\n')
        if post.is_mathjax:
            if use_katex:
                __M_writer(u'            <script src="//cdnjs.cloudflare.com/ajax/libs/KaTeX/0.3.0/katex.min.js"></script>\n            <script src="//cdnjs.cloudflare.com/ajax/libs/KaTeX/0.3.0/contrib/auto-render.min.js"></script>\n            <script>\n                renderMathInElement(document.body);\n            </script>\n')
            else:
                __M_writer(u'            <script type="text/javascript" src="//cdn.mathjax.org/mathjax/latest/MathJax.js?config=TeX-AMS-MML_HTMLorMML"> </script>\n            <script type="text/x-mathjax-config">\n            MathJax.Hub.Config({tex2jax: {inlineMath: [[\'$latex \',\'$\'], [\'\\\\(\',\'\\\\)\']]}});\n            </script>\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_open_graph_metadata(context,post):
    __M_caller = context.caller_stack._push_frame()
    try:
        lang = context.get('lang', UNDEFINED)
        permalink = context.get('permalink', UNDEFINED)
        url_replacer = context.get('url_replacer', UNDEFINED)
        striphtml = context.get('striphtml', UNDEFINED)
        abs_link = context.get('abs_link', UNDEFINED)
        blog_title = context.get('blog_title', UNDEFINED)
        use_open_graph = context.get('use_open_graph', UNDEFINED)
        __M_writer = context.writer()
        __M_writer(u'\n')
        if use_open_graph:
            __M_writer(u'    <meta property="og:site_name" content="')
            __M_writer(striphtml(unicode(blog_title)))
            __M_writer(u'">\n    <meta property="og:title" content="')
            __M_writer(filters.html_escape(unicode(post.title()[:70])))
            __M_writer(u'">\n    <meta property="og:url" content="')
            __M_writer(unicode(abs_link(permalink)))
            __M_writer(u'">\n')
            if post.description():
                __M_writer(u'    <meta property="og:description" content="')
                __M_writer(filters.html_escape(unicode(post.description()[:200])))
                __M_writer(u'">\n')
            else:
                __M_writer(u'    <meta property="og:description" content="')
                __M_writer(filters.html_escape(unicode(post.text(strip_html=True)[:200])))
                __M_writer(u'">\n')
            if post.previewimage:
                __M_writer(u'    <meta property="og:image" content="')
                __M_writer(unicode(url_replacer(permalink, post.previewimage, lang, 'absolute')))
                __M_writer(u'">\n')
            __M_writer(u'    <meta property="og:type" content="article">\n')
            if post.date.isoformat():
                __M_writer(u'    <meta property="article:published_time" content="')
                __M_writer(unicode(post.formatted_date('webiso')))
                __M_writer(u'">\n')
            if post.tags:
                for tag in post.tags:
                    __M_writer(u'           <meta property="article:tag" content="')
                    __M_writer(unicode(tag))
                    __M_writer(u'">\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


"""
__M_BEGIN_METADATA
{"source_encoding": "utf-8", "line_map": {"15": 0, "20": 2, "21": 11, "22": 23, "23": 40, "24": 69, "25": 85, "26": 102, "32": 13, "38": 13, "39": 14, "40": 15, "41": 16, "42": 17, "43": 18, "44": 18, "45": 18, "46": 18, "47": 18, "48": 21, "54": 25, "59": 25, "60": 26, "61": 27, "62": 28, "63": 29, "64": 30, "65": 30, "66": 30, "67": 30, "68": 30, "69": 30, "70": 33, "71": 34, "72": 35, "73": 35, "74": 35, "75": 35, "76": 35, "77": 35, "78": 38, "84": 71, "89": 71, "90": 72, "91": 73, "92": 73, "93": 73, "94": 74, "95": 75, "96": 75, "97": 75, "98": 76, "99": 77, "100": 77, "101": 77, "102": 79, "103": 80, "104": 80, "105": 80, "106": 81, "107": 82, "108": 82, "109": 82, "115": 3, "123": 3, "124": 4, "125": 5, "126": 6, "127": 7, "128": 7, "129": 7, "130": 7, "131": 7, "137": 87, "142": 87, "143": 88, "144": 89, "145": 90, "146": 95, "147": 96, "153": 42, "164": 42, "165": 43, "166": 44, "167": 44, "168": 44, "169": 45, "170": 45, "171": 46, "172": 46, "173": 47, "174": 48, "175": 48, "176": 48, "177": 49, "178": 50, "179": 50, "180": 50, "181": 52, "182": 53, "183": 53, "184": 53, "185": 55, "186": 60, "187": 61, "188": 61, "189": 61, "190": 63, "191": 64, "192": 65, "193": 65, "194": 65, "200": 194}, "uri": "post_helper.tmpl", "filename": "/home/ralsina/Desktop/proyectos/nikola/master/nikola/data/themes/base/templates/post_helper.tmpl"}
__M_END_METADATA
"""
