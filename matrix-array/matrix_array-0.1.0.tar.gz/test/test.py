'''
Created on 18 Sep, 2015

@author: wangyi
'''
import unittest
from matrix_array.array import *

from utils.parser import Parser

_report = []
_report2 = []

class const(object):
    _a = matrixArrayNum([
                         [['000', '001', '002'], ['010', '011', '012'], ['020', '021', '022']],
                         [['100', '101', '102'], ['110', '111', '112'], ['120', '121', '122']],
                         [['200', '201', '202'], ['210', '211', '212'], ['220', '221', '222']],
                         [['300', '301', '302'], ['310', '311', '312'], ['320', '321', '322']]
                         ])
    
    @staticmethod
    def get_b(rl, c):
        import  random
        import  time
        _b = matrixArrayNum(rl, c)

        start = time.time()   
          
        for i in range(rl):
            for j in range(c):
                #c = b[i,j]
                _b[i,j] = random.randrange(1, 1000)
                #d[i][j] = random.randrange(1, 1000)
                # print( b )
        elpse = time.time() - start
        _report2.append({'r':rl, 'c':c, 'elpse':elpse})
        return  _b

class Test(unittest.TestCase):


    def testName(self):
        pass
    
    
    def test_get(self):
        print("---Test 1: Basic Getter---")
        a = const._a; print("a:",a)
        result = []
        result.append("a[0]:")
        result.append(str(a[0]))
        result.append("a[1,1,1]:")
        result.append(str(a[1,1,1]))
        result.append("a[[1,2],[1,2]]:")
        result.append(str(a[[1,2],[1,2]]))
        result.append("[:,1]:")
        result.append(str(a[:,1]))
        result.append("[1,:]:")
        result.append(str(a[1,:]))
        result.append("[0,1],0:2,[1,0]")        
        result.append(str(a[[0,1],0:2,[1,0]]))
        
        print(Parser("get test: %s*", DELIMITER='\n').parse(result))
        print("---End of Test 1---")
        
    def test_set(self):
        pass
    
    def test_transform_vertically( self):
        print("---Test 2: Vertical Transformation---")
        a=const._a; print("a=%s\n 0 row <-> 1 row" % (a))      
        temp     = a[0,:,:]
        a[0,:,:] = a[1,:,:]
        a[1,:,:] = temp
        print("row transformation-0", a)
        
    def test_transform_horizontally(self):
        print("---Test 3: Horizontal Transformation---")
        a=const._a; print("a=%s\n 0 col <-> 1 col" % (a))
        temp     = a[:,0,0]
        a[:,0,0] = a[:,1,0]
        a[:,1,0] = temp
        print("col transformation-1", a)
        print("End of Test 2 & 3: Transformation")

    def test_add(self):
        print("---Test 4: Operator + ---")
        b = const.get_b(3, 3)
        c = (b[0,:] + b[1,:] + b[2,:]) / 3
        print('b=', b)
        print('b: (b0 + b1 + b2)/3 : --> c', c)
        d = b + 10
        print('b: b + 10: --> d', d)


    def test_mul(self):
        print("---Test 5: Operator * ---")
        print("b = Ax")
        A = const.get_b(8, 4)
        print("A=", A)
        x = const.get_b(4, 1)
        print("x=", x)
        b = A * x
        print("b=", b)
        import numpy as np
        A = np.array(A.tolist())
        x = np.array(x.tolist())
        print("numpy result:", A.dot(x))
        print("End of Operator testing") 

    def test_vt(self):
        print("---Test 6: Statistics ---")
        print("mean of col:")
        b = const.get_b(100, 10)
        print("b=\n", b)
        print(b.mean_vt())
        from numpy import array
        import numpy as np
        print("numpy result: \n%s" % np.mean(array(b.tolist()), axis=0))
        
    def test_ubds(self):
        print("variation of col:")
        b = const.get_b(100, 10)
        print("b=\n", b)
        print(b.ubds_vt())
        from numpy import array
        import numpy as np
        print("numpy result: \n%s" % np.std( array(b.tolist()), axis=0))
        print("End of Statistic Testing")
        
    def performance(self, r, c):
        
        import  random
        import  time
        
        result = {}
        
        b = const.get_b(r, c)
        
        start = time.time()   
          
        for i in range(r):
            for j in range(c):
                #c = b[i,j]
                b[i,j] = random.randrange(1, 1000)
                #d[i][j] = random.randrange(1, 1000)
                # print( b )
        elpse = time.time() - start
        result['PyMatrix/set'] = elpse
        
        for i in range(10):
            for j in range(10):
                b[i,j]#b._shape_array
        elpse = time.time() - start
        result['PyMatrix/get'] = elpse
        
        l = []
        start = time.time()
        for i in range(r):
            m = []
            for j in range(c):
                m.append(None)
            l.append(m)
             
        elpse = time.time() - start
        result['built-in append'] = elpse
         
        start = time.time()
        for i in range(r):
            for j in range(r):
                l[i][j]
             
        elpse = time.time() - start
        result['built-in set/get'] = elpse

        _report.append(result)
    
    def test_format(self):
        print("---Test 8: Formatting---")
        b = const.get_b(10, 10)

        e = matrixArray(b.tolist())
        e.setheader(['native', 'bound', 'I dont know', '1.00000000'])
        e.setheader([('sum',[0,1,2,3]),'know'])
        e[:,'sum']
        e.setIndice([1,2,3,4,5,6])
        e.setIndice([('first three rows', [0,1,2]), ('middle part', [3,4,5])])
        print(e[1:])
        print(e)

    
    def test_performance(self):
        print("---Test 7: Performance---")
        for i in range(10):
            self.performance(2**i, 2**i)
            
        print("####performance test####")
        print("ITME1:\n")
        table = matrixArray([])
        table.series(_report, ['PyMatrix/set', 'PyMatrix/get', 'built-in append', 'built-in set/get'])
        print(table)
        print("ITEM2:\n")
        table2= matrixArray([])
        table2.series(_report2, ['r', 'c', 'elpse'])
        print(table2)
        
    def testGJ(self):
        pass


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
    
