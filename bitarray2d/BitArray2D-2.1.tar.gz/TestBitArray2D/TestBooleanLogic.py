import BitArray2D
import BitVector
import unittest

ba1 = BitArray2D.BitArray2D( bitstring = '111\n101\n000' )
ba2 = BitArray2D.BitArray2D( rows = 3, columns = 3 )
ba3 = BitArray2D.BitArray2D( bitstring = '000\n010\n111' )

logicTests = [
    ((ba1,ba2, '&'), ba2),
    ((ba1,ba3, '&'), ba2),
    ((ba1,ba2, '|'), ba1),
    ((ba1,ba2, '^'), ba1),
    ((ba1,'', '~'), ba3),
    ]

class BooleanLogicTestCase(unittest.TestCase):
    def checkLogicOp(self):
        print("\nTesting Boolean operators") 
        for args, expected in logicTests:
            try:
                op = args[2]
                if (op == '&'):
                    actual = args[0] & args[1]
                elif (op == '|'):
                    actual = args[0] | args[1]
                elif (op == '^'):
                    actual = args[0] ^ args[1]
                elif (op == '~'):
                    actual =  ~args[0]
                assert actual == expected
            except Exception as e:
                if ( args[0].size == args[1].size ):
                    print(e)
                    print("        BOOLEAN LOGIC TEST FAILED")

def getTestSuites(type):
    return unittest.TestSuite([
            unittest.makeSuite(BooleanLogicTestCase, type)
                ])                    
