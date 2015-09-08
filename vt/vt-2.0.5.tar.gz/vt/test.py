import vt
a, at,i = vt.read_conf()
vt = vt.vtAPI(a)
print vt.getReport(*['search_intelligence', 'hashes'], **{'return_json':True, 'value':['behaviour:31.31.204.47']})