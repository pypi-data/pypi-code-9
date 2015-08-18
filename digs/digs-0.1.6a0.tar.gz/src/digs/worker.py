#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: Jonathan S. Prieto
# @Date:   2015-07-06 13:26:50
# @Last Modified by:   Jonathan Prieto
# @Last Modified time: 2015-07-07 01:45:07
from __future__ import print_function

from collections import defaultdict
import os
import string
from urlparse import urlparse, urljoin

from atxt.encoding import encoding_path
from atxt.formats import html
from atxt.formats._utils import save_raw_data, raw_data
from atxt.infofile import InfoFile
from atxt.utils import make_dir
from linkGrabber import Links
from logger import Logger


__all__ = ['scraper']

log = Logger.log
content_allow = ['text/plain', 'text/html']
tablereplace = '/.?&:=%'


def scraper(url, level_target=0, to=None, sameroot=False, overwrite=False):
    level = 0
    perlevel = defaultdict(list)
    perlevel[0].append(url)

    visited = defaultdict(int)
    visited[url] = True

    siteinfo = urlparse(url)
    total = defaultdict(int)  # total per level
    finished = 0

    while level  <= level_target:
        if not len(perlevel[level]) > 0:
            level += 1
            continue
        url_actual = perlevel[level].pop()
        msg = '[level:{}] [#:{}/{}]'
        idx = total[level] - len(perlevel[level])
        log.info(msg.format(level, idx, total[level]))
        log.info(url_actual)

        page = None
        dirpath = os.path.join(to, str(level))
        make_dir(dirpath)
        archivo = encoding_path(url_actual)

        for c in tablereplace:
            archivo = archivo.replace(c, '_')
        log.debug('using as filename:')
        archivo = os.path.join(dirpath, archivo)
        log.debug(archivo)

        try:
            from_file = InfoFile(archivo)
            txt_path = ''.join(
                [from_file.dirname, os.sep, from_file.name, '.txt'])
            to_txt = InfoFile(txt_path)

            try:
                page = Links(href=url_actual)
                links = page.find(duplicates=False)
            except Exception, e:
                log.error('[FAIL] %s' % e)
                continue

            if not page:
                log.info('The page apparently does not have links.')
                continue
            # process url
            if not overwrite and os.path.exists(to_txt.path):
                log.info('[OK] Text file already exists')
                finished += 1
            else:
                try:
                    save_text(from_file, to_txt, page.response.content)
                    log.info('[OK] Status: %s' % page.response.status_code)
                    finished += 1
                except Exception, e:
                    log.error(e)
                    log.error('[FAIL] Status: %s' %
                              page.response.status_code)

            print('urls added: ', end="")
            for _url in links:
                if 'href' not in _url:
                    continue
                _url = urljoin(url, _url['href'])
                if not visited[_url]:
                    visited[_url] = True
                    link = urlparse(_url)
                    if sameroot:
                        if link.netloc != siteinfo.netloc:
                            continue
                    perlevel[level + 1].append(_url)
                    total[level + 1] += 1
                    print('*', end="")

            print()
        except KeyboardInterrupt:
            log.info('process stopped')
            break

    # links_path = os.path.join(to, 'links.txt')
    # links = [u for u in visited.keys() if visited[u]]
    # save_raw_data(links_path, links, encoding=None)

    # log.info('Number of total urls: %s' % len(visited))
    log.info('Number of URLs saved: %s' % finished)


def save_text(from_file, to_txt, text):
    save_raw_data(from_file.path, text, encoding=None)
    html(from_file, to_txt, None)
    from_file.remove()
    return to_txt.path
