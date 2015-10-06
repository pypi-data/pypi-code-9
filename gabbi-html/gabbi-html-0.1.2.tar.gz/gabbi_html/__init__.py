__version__ = "0.1.2"


def gabbi_response_handlers():
    import gabbi.case
    from .response_handler import HTMLResponseHandler
    from .replacer import replace_response_html

    # monkey-patch gabbi to include custom replacer
    gabbi.case.REPLACERS += ["RESPONSE_HTML"]
    gabbi.case.HTTPTestCase._response_html_replace = replace_response_html

    return [HTMLResponseHandler]


def _parse_selector(selector):
    """
    extracts attribute name from selector, if any

    attributes are appended with `@<name>` (e.g. `a@href`)
    """
    attribute = None
    if "@" in selector:
        selector, attribute = selector.rsplit("@", 1)
    return selector, attribute
