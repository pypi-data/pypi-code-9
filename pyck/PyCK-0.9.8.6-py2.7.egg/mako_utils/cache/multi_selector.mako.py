# -*- coding:utf8 -*-
from mako import runtime, filters, cache
UNDEFINED = runtime.UNDEFINED
__M_dict_builtin = dict
__M_locals_builtin = locals
_magic_number = 10
_modified_time = 1436497934.838919
_enable_loop = True
_template_filename = '/MyWork/Projects/PyCK/pyck/mako_utils/templates/multi_selector.mako'
_template_uri = 'multi_selector.mako'
_source_encoding = 'utf8'
_exports = ['show_items']


def render_body(context,**pageargs):
    __M_caller = context.caller_stack._push_frame()
    try:
        __M_locals = __M_dict_builtin(pageargs=pageargs)
        def show_items(records,fname=None,ignore_prefix=None,indent='',parent_key=None):
            return render_show_items(context._locals(__M_locals),records,fname,ignore_prefix,indent,parent_key)
        items = context.get('items', UNDEFINED)
        field_name = context.get('field_name', UNDEFINED)
        ignore_prefix = context.get('ignore_prefix', UNDEFINED)
        __M_writer = context.writer()
        __M_writer(u'\n\n<script type="application/x-javascript">\n    //dojo.query(\'#main2 > input[type=checkbox]:checked\')\n    \n    function toggle_selection(chkbox, target_container){\n        require([ "dijit/registry", "dojo/query"], function(registry, query){  \n            query(target_container + " input").forEach(function(node, index, arr){\n              registry.byId(node.id).set("checked", registry.byId(chkbox).checked);\n            });\n          });\n    }\n</script>\n\n')
        __M_writer(unicode(show_items(items, field_name, ignore_prefix, '')))
        __M_writer(u'\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_show_items(context,records,fname=None,ignore_prefix=None,indent='',parent_key=None):
    __M_caller = context.caller_stack._push_frame()
    try:
        def show_items(records,fname=None,ignore_prefix=None,indent='',parent_key=None):
            return render_show_items(context,records,fname,ignore_prefix,indent,parent_key)
        isinstance = context.get('isinstance', UNDEFINED)
        dict = context.get('dict', UNDEFINED)
        __M_writer = context.writer()
        __M_writer(u'\n    ')

        extra_css_class = ""
        table_id = ''
        if parent_key:
            extra_css_class = 'collapse in'
            table_id = 'id="{}_subitems"'.format(parent_key)
        
        
        __M_writer(u'\n    \n    <table class="table table-condensed table-hover table-striped ')
        __M_writer(unicode(extra_css_class))
        __M_writer(u'" ')
        __M_writer(unicode(table_id))
        __M_writer(u'>\n')
        for k, v in records.items():
            __M_writer(u'        ')

            if ignore_prefix is not None and k.startswith(ignore_prefix):
                continue
            
            
            __M_writer(u'\n        \n')
            if not isinstance(v, dict):
                __M_writer(u'            <tr>\n                <td colspan="2">\n')
                if indent:
                    __M_writer(u'                    ')
                    __M_writer(unicode(indent))
                    __M_writer(u'\n')
                __M_writer(u'                    <input type="checkbox" data-dojo-type="dijit/form/CheckBox" name="')
                __M_writer(unicode(fname))
                __M_writer(u'" id="" value="')
                __M_writer(unicode(k))
                __M_writer(u'" />\n                    ')
                __M_writer(unicode(v))
                __M_writer(u'\n                </td>\n            </tr>\n')
            else:
                __M_writer(u'            <tr>\n                <td style="width: 4%;">\n                    <input data-dojo-type="dijit/form/CheckBox" id="')
                __M_writer(unicode(k))
                __M_writer(u'_parent" type="checkbox" onclick="toggle_selection(\'')
                __M_writer(unicode(k))
                __M_writer(u"_parent', '#")
                __M_writer(unicode(k))
                __M_writer(u'_subitems\');" />\n                </td>\n                <td data-toggle="collapse" data-target="#')
                __M_writer(unicode(k))
                __M_writer(u'_subitems">\n                    <b>')
                __M_writer(unicode(k))
                __M_writer(u'</b>\n                    <span class="glyphicon glyphicon-chevron-down"></span>\n                </td>\n            </tr>\n            <tr>\n                <td colspan="2">\n                    ')
                __M_writer(unicode(show_items(records=v, fname=fname, ignore_prefix=ignore_prefix, parent_key=k, indent=indent+'&nbsp;'*4)))
                __M_writer(u'\n                </td>\n            </tr>\n')
        __M_writer(u'    </table>\n    \n    \n')
        return ''
    finally:
        context.caller_stack._pop_frame()


"""
__M_BEGIN_METADATA
{"source_encoding": "utf8", "line_map": {"15": 0, "25": 48, "26": 62, "27": 62, "33": 1, "41": 1, "42": 2, "50": 8, "51": 10, "52": 10, "53": 10, "54": 10, "55": 11, "56": 13, "57": 13, "62": 16, "63": 18, "64": 19, "65": 21, "66": 22, "67": 22, "68": 22, "69": 24, "70": 24, "71": 24, "72": 24, "73": 24, "74": 25, "75": 25, "76": 28, "77": 29, "78": 31, "79": 31, "80": 31, "81": 31, "82": 31, "83": 31, "84": 33, "85": 33, "86": 34, "87": 34, "88": 40, "89": 40, "90": 45, "96": 90}, "uri": "multi_selector.mako", "filename": "/MyWork/Projects/PyCK/pyck/mako_utils/templates/multi_selector.mako"}
__M_END_METADATA
"""
