import time
import requests
import ujson

__author__ = 'Wu Fuheng'

class YahooData:
    def __init__(self, sym, f='2015'):
        to  = time.strftime("d=%m&e=%d&f=%Y")
        url = "http://ichart.finance.yahoo.com/table.csv?" \
              "s={sym}&a=00&b=05&c={f}&{to}&g=d&ignore=.csv".format(sym=sym,f=f,to=to)
        self.r   = requests.get(url)

    def getClosePrice(self):
        #print r.text
        d = []
        for i in self.r.text.split('\n')[1:]:
            v = i.split(',')
            if len(v[0])>0:
                t = time.strptime(v[0], "%Y-%m-%d")
                d.append([int(time.mktime(t)) * 1000, float(v[4])])
        d.reverse()
        return ujson.dumps(d)

if __name__ == '__main__':
    print YahooData('YY').getClosePrice()




