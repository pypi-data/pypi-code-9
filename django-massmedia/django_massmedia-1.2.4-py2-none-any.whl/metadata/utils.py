import re

regex_control_code = re.compile(r"([\x00-\x1f\x7f])")
controlchars = tuple({
    # Don't use "\0", because "\0"+"0"+"1" = "\001" = "\1" (1 character)
    # Same rease to not use octal syntax ("\1")
    ord("\n"): r"\n",
    ord("\r"): r"\r",
    ord("\t"): r"\t",
    ord("\a"): r"\a",
    ord("\b"): r"\b",
}.get(code, '\\x%02x' % code)
    for code in range(128)
)


def force_unicode(val, default_encoding='iso8859_1'):
    """
    Convert the string or list into utf8 values
    """
    if isinstance(val, basestring):
        try:
            return val.decode(default_encoding)
        except UnicodeDecodeError:
            val = regex_control_code.sub(lambda regs: controlchars[ord(regs.group(1))], val)
            val = re.sub(r"\\x0([0-7])(?=[^0-7]|$)", r"\\\1", val)
    elif isinstance(val, (list, tuple)):
        return [force_unicode(x) for x in val]
    return val
