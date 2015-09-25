import BitArray2D
import BitVector
import unittest

ba1 = BitArray2D.BitArray2D( bitstring = '001\n100\n111')
ba2 = BitArray2D.BitArray2D( rows = 2, columns = 2 )
ba3 = BitArray2D.BitArray2D( bitstring = '01101000\n01100101\n01101100\n01101100\n01101111')

constructorTests = [
    (( 'rowAndCol','2'), ba2 ), 
    (('bitstring', '001\n100\n111'), ba1 ),
    (('filename_char', 'testinput1.txt'), ba1 ),
    (('filename_bin', 'testinput2.dat'), ba3 )
    ]

class ConstructorTestCases(unittest.TestCase):
    def checkConstructors(self):
        print("\nTesting constructors")
        for args, expected in constructorTests:
            try:
                mode = args[0]
                if (mode == 'rowAndCol'):
                    ba = BitArray2D.BitArray2D( rows = eval(args[1]), \
                                  columns = eval(args[1]) )
                elif (mode == 'bitstring'):
                    ba = BitArray2D.BitArray2D( bitstring = args[1] )
                elif (mode == 'filename_char'):
                    ba   = BitArray2D.BitArray2D( filename = args[1] )
                    ba.read_bit_array_from_char_file()    
                elif (mode == 'filename_bin'):
                    ba   = BitArray2D.BitArray2D( filename = args[1] )
                    ba.read_bit_array_from_binary_file(rows=5,columns=8)
                actual = ba
                assert expected == actual
            except Exception as e:
                print(e)
                print("        CONSTRUCTOR TEST FAILED")

def getTestSuites(type):
    return unittest.TestSuite([
            unittest.makeSuite(ConstructorTestCases, type)
                ])                    
