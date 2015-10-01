import tinycss

from lxml import etree
from lxml.cssselect import CSSSelector
from lxml.html import soupparser

from linter import get_clients_without_support


# specificity is represented as a single int at the moment
# so to account for !important we need to make a big int
IMPORTANT_MULTIPLIER = 9000

def inline_css(html, css, strip_unsupported_css=True, remove_classes=False, pretty_print=True):
    """Produces html output with css styles inlined.

    :param html: the original html
    :param css: the css rules to apply to the html
    :param strip_unsupported_css: a flag for stripping invalid email css
    :param remove_classes: a flag for stripping class attributes from the output
    :param pretty_print: toggle pretty printing of resulting html
    """
    node_declarations = {}
    try:
        dom = etree.fromstring(html)
    except etree.XMLSyntaxError:
        # fall back on the soup parser if we don't have valid XML
        dom = soupparser.fromstring(html)

    css_rules = tinycss.make_parser().parse_stylesheet(css).rules
    for rule in css_rules:
        css_selector = rule.selector.as_css()
        for node in CSSSelector(css_selector)(dom):
            for declaration in rule.declarations:

                if strip_unsupported_css and get_clients_without_support(declaration):
                    # skip invalid rules
                    continue

                declaration.specificity = _selector_specificity(css_selector, declaration.priority)
                node_declarations.setdefault(node, {})
                active_declaration = node_declarations[node].get(declaration.name)
                if active_declaration and active_declaration.specificity > declaration.specificity:
                    # skip rules with lower specificity
                    continue

                node_declarations[node][declaration.name] = declaration

    for node, declarations in node_declarations.iteritems():
        inline_styles = node.get('style', '')
        inline_css = _get_node_style(declarations, inline_styles)
        node.set('style', inline_css)
        if remove_classes and "class" in node.attrib:
            node.attrib.pop('class')

    return etree.tostring(dom, pretty_print=pretty_print)


def _get_node_style(declarations, inline_styles):
    """Given css and inline styles determine the value of the style attribute."""
    inline_styles = _parse_style_attribute(inline_styles)
    stringify_value = lambda value: " ".join([v.as_css() for v in value])
    style = " ".join(["{}: {};".format(declaration.name, stringify_value(declaration.value)) \
                     for declaration in declarations.values() \
                     if declaration.name not in inline_styles])
    if inline_styles:
        if style:
            style = style + " "
        style = style + " ".join(["{}: {};".format(name, value) \
                                        for (name, value) in inline_styles.iteritems()])
    return style

def _parse_style_attribute(inline_styles):
    """Parse the style attribute value into a dict of css declarations."""
    inline_css = {}
    inline_styles = inline_styles.split(";")
    for rule in inline_styles:
        rule = rule.split(":")
        if len(rule) != 2:
            continue
        name, value = rule
        name = name.strip()
        value = value.strip()
        if name and value:
            inline_css[name] = value
    return inline_css

def _selector_specificity(selector, priority):
    """Calculate an integer representing selector specificity.

    The higher the number the more specific. This is a simplification of the
    spec, but works pretty well in practice.

    :param selector: the css selector
    :param priority: boolean that is set if the rule has the `!important` flag.
    """
    class_weight = selector.count(".")
    id_weight = selector.count("#")
    element_weight = len([a for a in selector.split(" ") if not (a.startswith(".") or a.startswith("#"))])
    weight = element_weight + class_weight * 10 + element_weight * id_weight * 100
    if priority:
        weight *= IMPORTANT_MULTIPLIER
    return weight
