import re
from os import listdir
from os.path import isfile, join

JEKYLL_FRONTMATTER_DELIM = "^---$"
NOAH_NODE = "[^\[\]]+"
NOAH_LINK = "\[\[(?P<node>" + NOAH_NODE + ")\]\]"

def split_frontmatter_and_body(fh):
    """
    Divide file contents between frontmatter and body
    Args:
        fh FileHandler
    Return:
        (frontmatter String, body String) Tuple

        Frontmatter & Body will be empty string if empty
    """
    lines = fh.readlines()
    frontmatter = ""
    body = ""

    # match opening '---'
    if lines and re.match(JEKYLL_FRONTMATTER_DELIM, lines[0]):
        for lino, line in enumerate(lines[1:], start = 1):
            # match ending '---'
            if re.match(JEKYLL_FRONTMATTER_DELIM, line):
                # will get all the lines except starting and ending '---'
                frontmatter = "".join(lines[1:lino])
                # body is remaining lines
                body = "".join(lines[lino+1:])
                break
    if not frontmatter:
        body = "".join(lines)
    return (frontmatter, body)

# === File

def get_all_files(path):
    return [ f for f in listdir(path) if isfile(join(path,f)) ]

# === File Contents

def get_all_links(fh):
    """
    Return:
        links List<String>
    """
    body = fh.read()
    return re.findall(NOAH_LINK, body)
