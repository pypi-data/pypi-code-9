# coding: utf-8

import requests
from optparse import OptionParser

QUERY_HOST = 'http://hq.sinajs.cn/'
USAGE = """
1. add a stock code
    stock sh600486
"""

def get_options():
    parser = OptionParser(usage=USAGE)
    parser.add_option("-c", "--code", dest="code", help="write stock code")

    (options, args) = parser.parse_args()

    return options, args

def main():
    options, args = get_options()
    code = options.code
    if not code:
        code = args[0]

    query_url = QUERY_HOST + 'list=%s' % code
    try:
        rest = requests.get(query_url)
        rst = rest.text
        infos = rst.split('=')[1].replace('"', '').split(',')
        name = infos[0]
        opening_price = infos[1]
        yesterday_closing_price = infos[2]
        current_price = infos[3]
        max_price = infos[4]
        min_price = infos[5]
        transaction_number = infos[6]
        transaction_amount = infos[7]
        print u'股票名:%s, 当前价格:%s' % (name, current_price)
    except Exception as e:
        print "Error:[%s]" % e

if __name__ == '__main__':
    main()






