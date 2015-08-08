import gettext


# The magic number is used by gettext to separate domains from
# messages.
MAGIC_NUMBER = '\x04'


def pgettext(domain, message):
    """Translatable string using `domain` and `message`."""
    translated = gettext.gettext(''.join([domain, MAGIC_NUMBER, message]))
    return translated if (MAGIC_NUMBER not in translated) else message
        
