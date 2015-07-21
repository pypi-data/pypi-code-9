class HeadersSettings(object):
    visible = {}
    """
    Headers set by ``.. code:: headers`` directive.

    Doesn't overwrite local headers, but are overwritten by CLI headers.

    :type: dict[str, str]
    """

    hidden = {}
    """
    Headers passed from command line. It overwrites all other headers,
    but are not visible in exported HTML file. Suitable for secret headers
    (like authentication credentials etc.)

    :type: dict[str, str]
    """
