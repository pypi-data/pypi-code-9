'''
.. module:: cascadict.sandbox
   :platform: Unix, Windows
   :synopsis: 
.. moduleauthor:: JNevrly

'''

from cascadict import CascaDict


a = {"a":1, "b":2, "c": {"ca": 1, "cb":2 }}
test1 = CascaDict(a)
 
 
test1['c']['cc'] = 3
#print test1
#print a
b = {'ba': 41, 'bb':42, "c": {"bca": 11, "bcb":22 }}
test2 = CascaDict(b)
test1.update(test2)
print test1
test3 = test1.cascade({'c':{'da':111, 'db':112} })
# test3 = test1.cascade()
# test3.update({'c':{'da':111, 'db':112} })
#test3['c'] = CascaDict({'da':111, 'db':112})
print test3
#print test3['c']['db']
# test4 = test3.cascade()
# test3['c']['ccc'] = 5
# print test4 
#   
# for (key, value) in test4.items():
#     print("{0}:{1}".format(key, value))