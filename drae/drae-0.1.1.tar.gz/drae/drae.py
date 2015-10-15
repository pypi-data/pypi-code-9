import requests
from bs4 import BeautifulSoup


# Use domain names? dle.rae.es
SEARCH_WORD_URL = "http://193.145.222.23/srv/search?w=%s"

class Word(object):
    FETCH_WORD_URL = "http://193.145.222.23/srv/fetch?id=%s"

    def __init__(self, word, id, text=None):
        self.word = word
        self.id = id
        self._text = text

    @property
    def text(self):
        if not self._text:
            response = requests.get(self.FETCH_WORD_URL % self.id)
            if response.status_code == 200:
                soup = BeautifulSoup(response.content)
                self._text = soup.article.get_text()
        return self._text

    def to_dict(self):
        return {'word': self.word, 'id': self.id, 'text': self.text}
    
    def __unicode__(self):
        return self.word

    def __repr__(self):
        return unicode(self).encode('utf-8')
    

def search(word):
    response = requests.get(SEARCH_WORD_URL % word)

    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')

        article = soup.article
        ul = soup.ul

        if article:
            word_id = article.get('id')
            text = article.get_text()
            return Word(word, word_id, text)
        elif ul:
            links = ul.find_all('a')
            return [Word(l.get_text()[:-1], l.get('href').split('=')[1]) for l in links]
