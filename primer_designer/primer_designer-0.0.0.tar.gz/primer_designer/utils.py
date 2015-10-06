import re


def is_fasta(filename):
    """Check if filename is fasta based on extension

    Return:
       Boolean
    """
    if re.search("\.fa*s[ta]*$", filename, flags=re.I):
        return True
    elif re.search("\.fa$", filename, flags=re.I):
        return True
    else:
        return False
