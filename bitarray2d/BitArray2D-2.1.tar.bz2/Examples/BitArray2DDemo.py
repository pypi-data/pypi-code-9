#!/usr/bin/env python

import BitArray2D
from BitArray2D import godel

print("\nConstructing an empty 2D bit array:")
ba = BitArray2D.BitArray2D( rows=0, columns=0 )
print(ba)

print("\nConstructing a bit array of size 10x10 with zero bits -- ba:")
ba = BitArray2D.BitArray2D( rows = 10, columns = 10 )
print(ba)

print("\nConstructing a bit array from a bit string -- ba2:")
ba2 = BitArray2D.BitArray2D( bitstring = "111\n110\n111" )
print(ba2)                    

print("\nPrint a specific bit in the array -- bit at 1,2 in ba2:")
print( ba2[ godel(1,2) ] )

print("\nSet a specific bit in the array --- set bit (0,1) of ba2:")   
ba2[0,1] = 0
print(ba2)

print("\nExperiments in slice getting and setting:")
print("Printing an array -- ba3:")
ba3 = BitArray2D.BitArray2D( bitstring = "111111\n110111\n111111\n111111\n111111\n111111" )
print(ba3)
ba4 = ba3[godel(2,3) : godel(4,5)]
print("Printing a slice of the larger array -- slice b4 of ba3:")
print(ba4)
ba5 = BitArray2D.BitArray2D( rows = 5, columns = 5 )
print("\nPrinting an array for demonstrating slice setting:")
print(ba5)
ba5[godel(2, 2+ba2.rows) : godel(2,2+ba2.columns)] = ba2
print("\nSetting a slice of the array - setting slice of ba5 to ba2:")
print(ba5)
print("\nConstructing a deep copy of ba, will call it ba6:")
ba6 = ba.deep_copy()
ba6[ godel(3,3+ba2.rows) : godel(3,3+ba2.columns) ] = ba2
print("Setting a slice of the larger array -- set slice of ba6 to ba2:")
print(ba6)

print("\nExperiment in bitwise AND:")
ba5 = ba.deep_copy()
ba7 = ba5 & ba6
print("Displaying bitwise AND of ba5 and ba6  --- ba7:")
print(ba7)

print("\nExperiment in bitwise OR:")
ba7 = ba5 | ba6
print("Displaying bitwise OR of ba5 and ba6  --- ba7:")
print(ba7)

print("\nExperiment in bitwise XOR:")
ba7 = ba5 ^ ba6
print("Displaying bitwise XOR of ba5 and ba6  --- ba7:")
print(ba7)

print("\nExperiment in bitwise negation:")
ba7 = ~ba5
print("Displaying bitwise negation of ba5 --- ba7:")
print(ba7)

print("\nSanity check (A & ~A => all zeros):")
print(ba5 & ~ba5)

print("\nConstruct bit array from a char file with ASCII 1's and 0's:" )
ba8 = BitArray2D.BitArray2D( filename = "data.txt" )
ba8.read_bit_array_from_char_file()
print("The bit array as read from the file -- ba8:")
print(ba8)

print("\nConstruct bit array from a packed binary file:")
ba9 = BitArray2D.BitArray2D( filename = "data_binary.dat" )
ba9.read_bit_array_from_binary_file(rows = 5, columns = 8)
print("The bit array as read from the file -- ba9:")
print("size of ba9: " + str(ba9.size()))
print(ba9)

print("\nTest the equality and inequality operators:")
ba10 = BitArray2D.BitArray2D( bitstring = "111\n110" )
ba11 = BitArray2D.BitArray2D( bitstring = "111\n110" )
print("ba10 is equal to ba11 is: " + str(ba10 == ba11))
ba12 = BitArray2D.BitArray2D( bitstring = "111\n111" )
print("ba10 is equal to ba12 is: " + str(ba10 == ba12))

print("\nTest shifting a bit array:")
print("printing ba13:")
ba13 = ba9.deep_copy()
print(ba13)
ba13.shift(rowshift=-2, colshift=2)
print("The shifted version of ba9:")
print(ba13)

print("\nTest dilation:")
ba14 = BitArray2D.BitArray2D( filename = "data2.txt" )
ba14.read_bit_array_from_char_file()
print("Array before dilation:")
print(ba14)
ba15= ba14.dilate(1)
print("Array after dilation:")
print(ba15)

print("\nTest erosion:")
ba16 = BitArray2D.BitArray2D( filename = "data2.txt" )
ba16.read_bit_array_from_char_file()
print("Array before erosion:")
print(ba16)
ba17= ba16.erode(1)
print("Array after erosion:")
print(ba17)

print("\nExperiments with writing array to char file:")
ba17.write_bit_array_to_char_file("out1.txt")

print("\nExperiments with writing array to packed binary file:")    
ba9.write_bit_array_to_packed_binary_file("out2.dat")

