#! /usr/bin/env python2.7
# coding=utf-8
__author__ = 'bulu_dog'
import requests
import multiprocessing
from bs4 import BeautifulSoup

# http://book.douban.com/subject_search?search_text=%E6%9C%BA%E5%99%A8%E5%AD%A6%E4%B9%A0&cat=1001
URL = 'http://book.douban.com/subject_search'


def search_book(query, page):
    """
    search book on book.douban.com and save these book's info
    :param query: query string
    :param page: the num of page
    :return: book url list
    """
    params = {
        'cat': 1001,
        'search_text': query,
        'start': page * 15
    }
    r = requests.get(URL, params=params)
    soup = BeautifulSoup(r.content, 'lxml')
    # 获取图书列表
    ul_soup = soup.findAll('div', attrs={'class': 'info'})
    book_list = []
    for item in ul_soup:
        a = item.a
        book_list.append(
            [
                a.get_text().replace('\n', '').replace(' ', ''),     # 标题
                a['href']                                           # URL
            ]
        )
    return book_list


def get_info_to_md(query):
    """
    get all books' info in first two search pages
    :param query:
    :return:
    """
    out_file = file("../" + query.decode('utf-8') + ".md", 'w')
    out_file.write("# " + query)
    out_file.write("  \n----  \n")
    # 进程池
    pool = multiprocessing.Pool(processes=4)
    # 默认抓取前两页的内容
    num = 1
    result = []
    for i in range(num):
        books = search_book(query, i)
        for book in books:
            name = book[0]
            url = book[1]
            result.append(pool.apply_async(get_single_book_info, (url, )))
    pool.close()
    pool.join()
    for item in result:
        item = item.get()
        name = item['name'].encode('utf-8')
        image = item['img']
        out_file.write("###{name}  \n".format(name=name))
        out_file.write("![{name}]({url})  \n".format(name=name, url=image))
    out_file.close()


def get_single_book_info(url):
    """
    获取指定url的book的信息
    :param url: url of the book
    :return: dict() - score - name - info
    """
    r = requests.get(url)
    soup = BeautifulSoup(r.content, 'lxml')
    name = soup.h1.get_text().replace(' ', '').replace('\n', '')
    info = soup.find('div', attrs={'id': 'info'})
    result = []
    for item in info.get_text().splitlines():
        item = item.strip()
        if len(item) > 1:
            result.append(item)
    score = soup.find('strong', attrs={'class': 'rating_num'})
    image = soup.find('div', attrs={'id': 'mainpic'})
    return dict(name=name,
                score=score.get_text().strip(),
                info=result,
                img=image.img['src'])

if __name__ == '__main__':
    get_info_to_md('数据挖掘')
