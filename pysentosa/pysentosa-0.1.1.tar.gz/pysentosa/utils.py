import config

__author__ = 'Wu Fuheng'

def __getLastPrice(s,tbl):
    cmd = "select dt,c from {} where s='{}' order by dt desc limit 1".format(tbl, s)
    r = config.CQuery().Query(cmd)
    if len(r)==0:
        return None, None
    return r.index[0], r.values[0][0]

def getLastPrice(s):
    tables = ['bar5s', 'bar15s']
    r = [__getLastPrice(s,t) for t in tables]
    t = None
    p = None
    for i in r:
        if t==None:
            t = i[0]
            p = i[1]
        elif i[0] > t:
            t = i[0]
            p = i[1]
    return p, t

if __name__ == "__main__":
    print getLastPrice('NQ')
    print getLastPrice('NG')