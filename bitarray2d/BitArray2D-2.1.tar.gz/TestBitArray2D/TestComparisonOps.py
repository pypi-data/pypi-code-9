import BitArray2D
import BitVector
import unittest

ba1 = BitArray2D.BitArray2D( bitstring = '111\n101\n000' )
ba2 = BitArray2D.BitArray2D( bitstring = '111\n101\n000' )
ba3 = BitArray2D.BitArray2D( rows = 3, columns = 3 )
ba4 = BitArray2D.BitArray2D( bitstring = '000\n010\n111' )


comparisonTests = [
    ((ba1,ba2, '=='), True),
    ((ba1,ba2, '!='), False),
    ((ba1,ba3, '=='), False),
    ((ba1,ba3, '!='), True),
    ]

class ComparisonTestCases(unittest.TestCase):
    def checkComparisons(self):
        print("\nTesting comparison operators")
        for args, expected in comparisonTests:
            try:
                op = args[2]
                if (op == '=='):
                    actual = args[0] == args[1]
                elif (op == '!='):
                    actual = args[0] != args[1]
                assert expected == actual
            except Exception as e:
                print(e)
                print("        COMPARISON TEST FAILED")

def getTestSuites(type):
    return unittest.TestSuite([
            unittest.makeSuite(ComparisonTestCases, type)
                             ])                    
