import math
import hashlib
import random

try: 	
    import bitarray
except ImportError: 
    raise ImportError('pyPBF requires bitarray')

try: 
    import mmh3
except ImportError:
    raise ImportError('pyPBF requires mmh3')

__version__ = '0.0.0'
__author__ = 'Sisi Xiong'

#Generate a set of hash values, module by the size
def makeHashFuncs(key, size, numHashes):
    hashValue = []
    for i in range(1, (numHashes+1)):
        value = mmh3.hash(key,i) % size
        #print value
        hashValue.append(value)
    return hashValue

class PBF(object):
    #Parameter initialization
    def __init__(self,n,f,k=200):
        if not (n > 0):
            raise ValueError("Number of items must be > 0")
        if not (f > 0):
            raise ValueError("Threshold frequency much be > 0")
        if not (n > f):
            raise ValueError("Number of items should be larger than threshold frequency")
        if not (k > 150):
            raise ValueError("Number of hash functions must be > 150")
        # n : Desigend total number of items
        # f : Threshold frequency
        # m : The size of the PBF, the lenght of PBF vector
        # p : Preset probability
        # k : Number of hash functions
        # count : Number of items inserted
        # bitarray : PBF vector
        self.n = n
        self.f = f
        self.k = k
        e = 0.1
        p = ((n - f)*math.log(1-e) - n*math.log(e))/n/f
        m = -k*n*p/math.log(1-e)
        m = int(math.ceil(m))
        self.p = p
        self.m = m
        self.count = 0 
        self.bitarray = bitarray.bitarray(self.m)
        self.bitarray.setall(False)
        print "n = "+str(n)+", f = "+str(f)+", k = "+str(k)+", m = "+str(m)+", p = "+str(p)
    
    #Insert item
    def insert(self,item):
        if self.count >= self.n :
            print "Exceed capacity!"
            return False
        else :
            self.count += 1 
            m = self.m
            k = self.k
            p = self.p
            hashValue = makeHashFuncs(item,m,k)
            for i in hashValue:
                temp = round(random.uniform(0.0,1.0),10)
                #print temp
                if(temp < p):
                    self.bitarray[i] = True
            return True

    #Return how many items have been inserted
    def numItems(self):
        return self.count

    #Query item, count number of 1s
    def queryCount(self,item):
        result = 0
        m = self.m
        k = self.k
        hashValue = makeHashFuncs(item,m,k)
        for i in hashValue:
            result += self.bitarray[i]
        #print result
        return result

    #Calculate frequency result
    def calFreq(self,result):
        k = self.k
        if result == k :
            print 'result = '+str(result)
            result = k-1
        p = self.p
        m = self.m
        n = self.count
        #n = self.n
        #print 'k = '+str(k)+' p = '+str(p)+' n = '+str(n)
        tempa = k*p*n + m*math.log(1-float(result)/k)
        tempb = (k-m)*p
        frequency = tempa / tempb
        return frequency
    
    #Query frequency directly
    def queryFreq(self,item):
        count = self.queryCount(item)
        frequency = self.calFreq(count)
        #print frequency
        return int(round(frequency))

if __name__ == "__main__":
    pbf = PBF(n=1000,f=50)
    for i in range(1,50):
        pbf.insert('foo')
    count = pbf.numItems
    freq = pbf.queryFreq('foo')
    
