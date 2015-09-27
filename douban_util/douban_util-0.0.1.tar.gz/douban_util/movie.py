# coding=utf-8
__author__ = 'bulu_dog'
import requests
import multiprocessing
from bs4 import BeautifulSoup

URL = 'http://movie.douban.com/subject_search'

# http://movie.douban.com/subject_search
# ?search_text=%E5%81%B7%E6%8B%90%E6%8A%A2%E9%AA%97&cat=1002
def search_for_movie_page(query):
    """
    在豆瓣电影中查找电影，并返回第一条结果的URL
    :param query -- the movie what u want to search on douban.com
    :param page
    """
    params = {
        'search_text': query,
        'cat': 1002
    }
    r = requests.get(URL, params=params)
    soup = BeautifulSoup(r.content, "lxml")
    item_list = soup.find_all('tr', attrs={'class': 'item'})
    if len(item_list) > 0:
        #获取搜索到内容的第一条URL
        item = item_list[0]
        info_page_url = item.a['href']
        if info_page_url:
            return info_page_url
        else:
            return None
    else:
        return None

def search_for_movie_cat(url):
    if url is None:
        return None
    page_r = requests.get(url)
    soup = BeautifulSoup(page_r.content, 'lxml')
    # title
    #print soup.h1.find()
    # info box
    info = soup.find('div', attrs={'id': 'info'})
    spans = info.find_all('span', attrs={'property':'v:genre'})
    if not spans:
        return None
    cat = []
    for span in spans:
        cat.append(span.get_text())
    return cat

if __name__ == "__main__":
    for item in search_for_movie_cat(search_for_movie_page('星球大战')):
        print item
