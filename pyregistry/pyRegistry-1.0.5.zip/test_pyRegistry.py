import sys

sys.path[0:1] = ['./build/lib.win32-%s.%s' % sys.version_info[0:2]]

import pyRegistry
reg = pyRegistry.open('HKLM\\Software')
key_count = len(reg.getKeyNames())
print key_count, " items returned from getKeyNames()"
n = 0
for i in reg :
    #print i
    n += 1
    #if n == 10 : break

if n == key_count :
    print 'iteration count matches getKeyNames() list'
else :
    print 'uh-oh, iteration does not match getKeyNames() list'


