def headers_as_string(headers, line_separator='\n'):
    """
    :param headers: Dictionary with headers.
    :type headers: dict
    """
    return line_separator.join(
        ['{}: {}'.format(k, v) for k, v in headers.items()]
    )
