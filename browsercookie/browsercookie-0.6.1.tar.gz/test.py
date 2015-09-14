# -*- coding: utf-8 -*-

import __init__ as common
import urllib2

def main():
    cj = common.chrome()
    #cj = common.firefox()
    opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
    url = 'http://stackoverflow.com/'
    #print 'hoju' in urllib2.urlopen(url).read()
    html = opener.open(url).read()
    print 'hoju' in html
    open('test.html', 'w').write(html)


if __name__ == '__main__':
    main()

