## -*- coding: utf-8 -*-

import markdown as md


def preprocessing(s):
    """
    Returns string where \\ is replaced by \\\ so that latex new lines work
    """
    return  s.replace(r'\\', r'\\\\')


def md_to_html(text_md):
    """
    Returns HTML string
    The input string should be of the raw 'r' type
    """

    css = """
    <style>
    
    /* To position Latex MathJax expressions - otherwise left-aligned by default */

    div.output_area .math_center .MathJax_Display {
        text-align: center !important;
    }

    div.output_area .math_right .MathJax_Display {
        text-align: right !important;
    }


    /* To center markdown table - otherwise left-aligned by default */

    div.output_area .rendered_html .table_center table {
        margin: auto;
    }

    
    </style>
    """

    html = md.markdown(preprocessing(text_md).decode('utf-8'),
                       extensions=['markdown.extensions.tables'])

    return css+html

