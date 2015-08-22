from bs4 import BeautifulSoup

def format (s):
    return "html", BeautifulSoup(s, ).prettify()
