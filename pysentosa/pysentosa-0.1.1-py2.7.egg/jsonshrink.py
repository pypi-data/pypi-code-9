__author__ = 'root'
import ujson
'''
json={p,p...}|non-pair-non-list|[v,v,...]
p=str:v
v=non-pair-non-list|json|p|[v,v,...]
'''

t0 = ujson.loads("[1,2,3]")
t1 = ujson.loads("3")

def NDNL(x):
    return not isinstance(x,dict) and not isinstance(x,list)

def shrinkdict(x):
    if len(x)==0:
        return None

    r={}
    for (k,v) in x.iteritems():
        if NDNL(v) and v is not None:
            r[k] = v
        elif isinstance(v,dict):
            y = shrinkdict(v)
            if y is not None:
                r[k] = y
        elif isinstance(v,list):
            y = shrinklist(v)
            if y is not None:
                r[k] = y
    if len(r)==0:
        return None
    else:
        if len(r)==1 and (r.keys()[0]=='sym' or r.keys()[0]=='syms'):
            return None
        return r

def shrinklist(x):
    if len(x)==0:
        return None
    r=[]
    for i in x:
        if NDNL(i):
            if i is not None:
                r.append(i)
        elif isinstance(i,dict):
            y = shrinkdict(i)
            if y is not None and len(y)!=0:
                r.append(y)
        elif isinstance(i,list):
            y = shrinklist(i)
            if y is not None and len(y)!=0:
                r.append(y)
    if len(r) == 0:
        return None
    else:
        return r

#return a shrunk json object
def shrink(json):
    if isinstance(json,dict):
        return shrinkdict(json)
    elif isinstance(json,list):
        return shrinklist(json)
    else:
        return json


if __name__=="__main__":
    print shrink(t1)
    print shrink(t0)