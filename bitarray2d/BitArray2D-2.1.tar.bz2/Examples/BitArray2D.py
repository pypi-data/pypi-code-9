#!/usr/bin/env python

__version__ = '2.1'
__author__  = "Avinash Kak (kak@purdue.edu)"
__date__    = '2011-March-22'
__url__     = 'http://RVL4.ecn.purdue.edu/~kak/dist2d/BitArray2D-2.1.html'
__copyright__ = "(C) 2011 Avinash Kak. Python Software Foundation."

__doc__ = '''

    BitArray2D.py

    Version: ''' + __version__ + '''
   
    Author: Avinash Kak (kak@purdue.edu)

    Date: ''' + __date__ + '''

    @title
    CHANGE LOG:

      Version 2.1:

          BitArray2D is a renamed version of Bit2DArray.  This name change
          was made in response to user requests.  BitArray2D is Python 3.x
          compliant. It should work with both Python 2.x and Python 3.x.


    @title
    INSTALLATION:

       The BitArray2D class was packaged using Distutils.  For
       installation, execute the following command-line in the source
       directory (this is the directory that contains the setup.py file
       after you have downloaded and uncompressed the tar archive):
 
           python setup.py install

       You have to have root privileges for this to work.  On Linux
       distributions, this will install the module file at a location that
       looks like

            /usr/lib/python2.7/site-packages/

       If you do not have root access, you have the option of working
       directly off the directory in which you downloaded the software by
       simply placing the following statements at the top of your scripts
       that use the BitArray2D class

           import sys
           sys.path.append( "pathname_to_BitArray2D_directory" )

       To uninstall the module, simply delete the source directory, locate
       where BitArray2D was installed with "locate BitArray2D" and delete
       those files.  As mentioned above, the full pathname to the installed
       version is likely to look like
       /usr/lib/python2.6/site-packages/BitArray2D*

       If you want to carry out a non-standard install of BitArray2D, look
       up the on-line information on Disutils by pointing your browser to

              http://docs.python.org/dist/dist.html


    @title
    INTRODUCTION:
   
       The BitArray2D class is for a memory-efficient packed representation
       of 2D bit arrays and for logical and other operations (such as blob
       dilations, erosions, etc.) on such arrays. The implementation of the
       class takes advantage of the facilities of the BitVector class for
       the memory representation and for the allowed operations.

       Operations supported on 2D bit arrays:

            __str__
            __getitem__
            __setitem__
            __getslice__
            __eq__
            __ne__
            __and__
            __or__
            __xor__
            __invert__
            deep_copy
            size
            read_bit_array_from_char_file
            read_bit_array_from_binary_file
            write_bit_array_to_char_file
            write_bit_array_to_packed_binary_file
            shift
            dilate
            erode

    @title
    CONSTRUCTING 2D BIT ARRAYS:

        You can construct a 2D bit array in four different ways:
   
        (1) You can construct a packed 2D bit array of all zeros by a
            call like

                ba = BitArray2D( rows = 20, columns = 10 )

            This will create a 2D array of size 20x10.  You can then set
            the individual bits in this array using syntax that is shown
            later in this documentation.

            The following call will return an empty BitArray2D instance:

                ba = BitArray2D( rows=0, columns=0 )
 
        (2) You can construct a 2D bit array from a string in the following
            manner:

                ba = BitArray2D( bitstring = "111\n110\n011" )

            This will create the following bit array in the memory:

                     111
                     110
                     011

            There is no limit on the either the row size or the column size
            of the bit array created in this manner.  However, the rows
            must all be of exactly the same size.  An exception is thrown
            when that condition is violated.

            Note that even though you are supplying to the BitArray2D
            constructor a string made of ASCII 1's and 0's, the 2D bit
            array that is created is stored in a packed form.  So a row
            with, say, sixteen 1's and/or 0's will be stored as just two
            bytes in the memory. So a 16x16 bit array will occupy only 
            32 bytes in the memory.


        (3) You can create a 2D bit array by reading the bits directly from
            a text file by calls that look like

                ba = BitArray2D( filename = "data.txt" )
                ba.read_bit_array_from_char_file()

            You first have to create an empty BitArray2D instance, as in
            the first statement above, and then call the method
            read_bit_array_from_char_file() on the instance.

            Even though the text file supplies ASCII 1's and 0's, the
            internal representation of the bit array will be packed, as
            mentioned for the case (2) above.

            Note that when you create a bit array in this manner, the 
            newline character in the text file is used as a row delimiter. 


        (4) You can create a 2D bit array by reading the bits directly from 
            a binary file through calls like:

                ba = BitArray2D( filename = "data_binary.dat" )
                ba.read_bit_array_from_binary_file(rows = 5, cols = 8)

            Since you are creating a bit array from a binary file, you
            cannot designate any particular byte as a row delimiter. That's
            the reason for why you must now specify the number of rows and
            the number of columns to the read method in the second
            statement.  If the number of bits in the binary file is less
            than what you need for the 2D bit array in the second statement
            above, an exception is thrown.

            To illustre creating a bit array by reading a file in the binary
            mode, assume that the file has the characters 'hello' in it
            and you read this file into a bit array by calling:

                ba = BitArray2D( filename = "hello_file.dat" )
                ba.read_bit_array_from_binary_file(rows = 5, cols = 8)
            
            If you now say

                print ba

            you will see the following array displayed in your terminal
            window:

                          01101000
                          01100101
                          01101100
                          01101100
                          01101111

            These are the ASCII representations of the characters 'h', 'e',
            'l', 'l', and 'o'.

    @title   
    OPERATIONS SUPPORTED BY THE BitArray2D CLASS:
    
    @title
    DISPLAYING BIT ARRAYS:


       (5)  Since the BitArray2D class implements the __str__ method, a bit
            array can be displayed in a terminal window by

                  print( ba )

            where ba is an instance of BitArray2D. This will display in
            your terminal window the bit array ba, with each row of the
            array in a separate line. (Obviously, this is not what you
            would do for very large bit arrays. But, for diagnostic work,
            such displays can be very helpful.) You can always obtain the
            string representation of a bit array by

                  str( ba )

            In the string representation, the rows are separated by the
            newline character.


    @title
    ACCESSING AND SETTING INDIVIDUAL BITS AND SLICES:

   
       (6)  You can access any individual bit of a 2D bit array by

                  bit = ba[ godel(i,j) ] 

            The call on the right will return the bit in the i-th row and
            the j-th column of the BitArray2D ba.  This assumes that you
            have specifically imported the name 'godel' from the BitArray2D
            module.  If that is not the case, the above call will look like

                  bit = ba[ BitArray2D.godel(i,j) ] 

            The function godel(a,b) is used to map a pair of integers a and
            b into a unique integer with the help of the Godel pairing
            formula.

            
       (7)  Any single bit of a bit array ba at row index i and column index
            j can be set to 1 or 0 by

                  ba[i,j] = 1_or_0



       (8)  A slice of a bit array, defined by the corner coordinates (i,j)
            and (k,l), can be retrieved by

                from BitArray2D import godel

                ba[ godel(i,j) : godel(k,l) ]
 
            In the implementation of the __getslice__ method that handles
            the above invocation, calls to ungodel(m) are used to recover
            the components i and j of a pair whose Godel map is m.  To
            demonstrate the working of slice retrieval:

                ba1 = BitArray2D( bitstring = \
                     "111111\n110111\n111111\n111111\n111111\n111111" )
                ba2 = ba3[godel(2,3) : godel(4,5)]
                print( ba4 )

            yields 
      
                11
                11

       (9)  You can also carry out slice assignment by using syntax like

                from BitArray2D import godel
                ba1[ godel(i,j) : godel(k,l) ]  =  ba2               

            where the 2D bit array ba1 is presumably larger than the 2D bit
            array ba2.  The above call will replace the rectangular region
            of ba1 that is defined by the corner coordinates (i,j) and
            (k,l) by the bit array ba2, assuming that that the row width of
            ba2 is (k-i) and the column width (l-j).  So in a call like

                ba1 = BitArray2D( bitstring = "101\n110\n111" )   # 101
                                                                  # 110
                                                                  # 111
                ba2 = BitArray2D( rows = 5, columns = 5 )     # 00000
                                                              # 00000
                                                              # 00000
                                                              # 00000
                                                              # 00000
                ba2[ godel(2, 2+ba2.rows) : godel(2,2+ba2.columns) ] = ba1
                print( ba2 )                                  # 00000
                                                              # 00000
                                                              # 00101
                                                              # 00110
                                                              # 00111

       (10) You can construct a deep copy of a bit array by

                ba2 = ba1.deep_copy()

            The bit array in ba2 will exactly the same as in ba1, except
            that the two bit arrays will be two different objects in the
            memory.

    @title
    LOGICAL OPERATIONS ON 2D BIT ARRAYS:


       (11) You can carry out all of the logical operations on 2D bit arrays:

              result_ba =  ba1 & ba2                    # for bitwise AND
          
              result_ba =  ba1 | ba2                    # for bitwise OR

              result_ba =  ba1 ^ ba2                    # for bitwise XOR

              result_ba =  ~ ba                         # for bitwise negation

    @title
    COMPARING 2D BIT ARRAYS:

       (12) Given two 2D bit arrays, you can test for equality and inequality
            through the following boolean comparisons:

              ba1 == ba2

              ba1 != ba2

    @title
    OTHER SUPPORTED OPERATIONS:

       (13) You can shift a bit array array by

              ba.shift( rowshift = m, colshift = n )

            where m is the number of positions row-wise by which you
            want to shift the array and the n the same column-wise.

            The values for m and n are allowed to be negative.  A positive
            value for m will cause a bit array to shift downwards and a
            positive value for n to shift rightwards.

            What may make this method confusing at the beginning is the
            orientation of the positive row direction and the positive
            column direction.  The origin of the array is at the upper left
            hand corner of your display.  Rows are positive going downwards
            and columns are positive going rightwards:
 
                       X----->  +ve col direction
                       |
                       |
                       |
                       V
                  +ve row direction

            So a positive value for rowshift will shift the array downwards
            and a positive value for colshift will shift it rightwards.
            Just remember that if you want the shifts to seem more
            intuitive, use negative values for the rowshift argument.


       (14) In order to patch small holes, you can dilate the blobs made up
            of 1's that are connected through neighborhood relationship by
            calling dilate():

                result_ba  =  ba.dilate( m )

            The returned bit array is an OR of the bit arrays obtained by
            shifting ba by m positions in all four cardinal directions.


       (15) The opposite of dilate is erode. An erosion operation should
            shrink the blobs by the deletion of 1's that are at the boundary
            up to a depth determined by the argument supplied to erode():

                result_ba  =  ba.erode( m )

            Logically, the array returned by the above call is an AND of
            the the bit arrays obtained by shifting ba by m positions in
            each of the four cardinal directions.


       (16) You can write a bit array directly to a text file if you want
            the bits to be written out as ASCII 1's and 0's:  

                ba.write_bit_array_to_char_file("out_file.txt")

            This can be a useful thing to do when you are playing with
            small to medium sized bit arrays.  This call will deposit the
            newline character at the end of each row of the bit array.
            Subsequently, you can re-create the bit array in the memory by
            reading the file with the calls

                ba = BitArray2D( filename = "filename.txt" )
                ba.read_bit_array_from_char_file() 

            that were mentioned earlier in item (3) above.


       (17) You can write a bit array in its packed binary representation
            to a file (that would obviously be a binary file) by calling

                ba.write_bit_array_to_packed_binary_file("filename.dat")

            The overall size of bit array ba must be a multiple of 8 for
            this write function to work.  If this condition is not met, the
            function will throw an exception.

            When writing an internally generated bit array out to a disk
            file, the implementation of the write function opens the file
            in the binary mode.  This is particularly important on Windows
            machines since, if the file were to be opened in the text mode,
            the bit pattern 00001010 ('\\n') in a bit array will be written
            out as 0000110100001010 ('\\r\\n').

            A binary file created by the above call can be read back into
            the memory by the calls shown in item (4) above:

                ba = BitArray2D( filename = "filename.dat" )
                ba.read_bit_array_from_binary_file(rows = 5, cols = 8)

            As mentioned in (4) above, since no bytes can serve as row
            delimiters for binary files, you have to tell the read function
            how many rows and columns to read off the file.


    @title
    HOW A BIT ARRAY IS STORED:
   
        Through the facilities provided by the BitVector class, the bits of
        a bit array are stored in 16-bit unsigned ints.  

    @title
    ABOUT THE AUTHOR:

        Avi Kak is the author of "Programming with Objects: A Comparative
        Presentation of Object-Oriented Programming with C++ and Java",
        published by John-Wiley in 2003. This book presents a new approach
        to the combined learning of two large object-oriented languages,
        C++ and Java.  It is being used as a text in a number of
        educational programs around the world.  This book has also been
        translated into Chinese.  Avi Kak is also the author of "Scripting
        with Objects: A Comparative Presentation of Object-Oriented
        Scripting with Perl and Python," published in 2008 by John-Wiley.


    @title
    SOME EXAMPLE CODE:

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
        

        (For a more complete working example, see the
         example code in the BitArray2DDemo.py file in the
         Examples sub-directory.)

'''

from BitVector import __version__ as bitvector_version
if bitvector_version.split('.')[0] < '3':
    raise ImportError("The imported BitVector module must be of version 3.0 or higher")

import BitVector
import re

class BitArray2D( object ):                                          #(A1)

    def __init__( self, *args, **kwargs ):                           #(A2)
        if args:                                                     #(A3)
               raise ValueError(                                     #(A4)
                      '''BitArray2D constructor can only be called with
                         keyword arguments for the following keywords:
                         rows, columns, filename, bitstring)''')    
        allowed_keys = 'bitstring','filename','rows','columns'       #(A5)
        keywords_used = kwargs.keys()                                #(A6)
        for keyword in keywords_used:                                #(A7)
            if keyword not in allowed_keys:                          #(A8)
                raise ValueError("Wrong keyword used")               #(A9)
        filename = rows = columns = bitstring = None                #(A10)

        if 'filename' in kwargs  : filename  = kwargs.pop('filename')
        if 'rows' in kwargs      : rows      = kwargs.pop('rows')
        if 'columns' in kwargs   : columns   = kwargs.pop('columns')
        if 'bitstring' in kwargs : bitstring = kwargs.pop('bitstring')
                                                             #(A11 -- A14)
        self.filename  = None                                       #(A15)
        self.rows      = None                                       #(A16)
        self.columns   = None                                       #(A17)
        self.bitstring = None                                       #(A18)
        self.FILEIN    = None                                       #(A19)

        if filename:                                                #(A20)
            if rows or columns or bitstring:                        #(A21)
                raise ValueError(                                   
                  '''When filename is specified, you cannot
                     give values to any other constructor args''')  #(A22)
            self.filename = filename                                #(A23)
            self.rowVectors = []; self.rows = 0; self.columns = 0   #(A24)
            import sys                                              #(A25)
            try:                                                    #(A26)
                if sys.version_info[0] == 3:                        #(A27)
                    self.FILEIN = open( filename, encoding='utf-8' )#(A28)
                else:                                               #(A29)
                    self.FILEIN = open( filename, 'rb' )            #(A30)
            except IOError as e:                                    #(A31)
                print(e.strerror)                                   #(A32)
            return                                                  #(A33)
        elif rows is not None and rows >= 0:                        #(A34)
            if filename or bitstring:                               #(A35)
                raise ValueError(                              
                  '''When number of rows is specified, you cannot
                     give values to any other constructor args except
                     for columns''')                                #(A36)
            if not columns >= 0:                                    #(A37)
                raise ValueError(
                  '''When number of rows is specified, you must also
                     specify a value for the number of columns''')  #(A38)
            self.rows = rows; self.columns = columns                #(A39)
            self.rowVectors = [ BitVector.BitVector( size = self.columns ) \
                                   for i in range( self.rows ) ]    #(A40)
            return                                                  #(A41)
        elif bitstring or bitstring == '':                          #(A42)
            self.rowVectors = [ BitVector.BitVector( bitstring = bits ) \
                         for bits in re.split( '\n', bitstring ) ]  #(A43)
            self.rows = len( self.rowVectors )                      #(A44)
            self.columns = self.rowVectors[0].length()              #(A45)
            rowVecSizes = [ len(x) for x in self.rowVectors ]       #(A46)
            if max( rowVecSizes ) != min( rowVecSizes ):            #(A47)
                raise AttributeError("Your row sizes do not match") #(A48)

    def _add_row(self, bitvector):                                   #(B1)
        if self.columns == 0:                                        #(B2)
            self.columns = bitvector.length()                        #(B3)
        elif self.columns != bitvector.length():                     #(B4)
            raise ValueError("Size wrong for the new row")           #(B5)
        self.rowVectors.append( bitvector )                          #(B6)
        self.rows += 1                                               #(B7)
        
    def __str__( self ):                                             #(C1)
        'To create a print representation'
        if self.rows==0 and self.columns==0:                         #(C2)
            return ''                                                #(C3)
        return '\n'.join( map( str, self.rowVectors ) )              #(C4)

    def __getitem__( self, pos ):                                    #(D1)
        'Get the bit from the designated position'
        if not isinstance( pos, slice ):                             #(D2)
            row,col = ungodel(pos)                                   #(D3)
            if  row >= self.rows or row < -self.rows:                #(D4)
                raise ValueError( "row index range error" )          #(D5)
            if  col >= self.columns or col < -self.columns:          #(D6)
                raise ValueError( "column index range error" )       #(D7)
            if row < 0: row = self.rows + row                        #(D8)
            if col < 0: col = self.columns + col                     #(D9)
            return self.rowVectors[row][col]                        #(D10)
        else:                                                       #(D11)
            if pos.start is None:                                   #(D12)
                start = 0,0                                         #(D13)
            else:                                                   #(D14)
                start = ungodel(pos.start)                          #(D15)
            if pos.stop is None:                                    #(D16)
                stop = self.rows,self.columns                       #(D17)
            else:                                                   #(D18)
                stop = ungodel(pos.stop)                            #(D19)
            result = BitArray2D( rows=0, columns=0 )                #(D20)
            for i in range( start[0], stop[0] ):                    #(D21)
                result._add_row( BitVector.BitVector( bitstring = \
                      str(self.rowVectors[i][start[1]:stop[1]])) )  #(D22)
            return result                                           #(D23)

    def __setitem__(self, pos, item):                                #(E1)
        '''
        This is needed for both slice assignments and for index-based
        assignments.  It checks the type of pos and item to see if the call
        is for slice assignment.  For slice assignment, the second argument
        must be of type slice '[m:n]' whose two numbers m and n are
        produced by calling godel() on the two corners of the rectangular
        regions whose values you want to set by calling this function.  So
        for slice assignments, think of pos as consisting of
        '[(i,j):(k,l)]' where (i,j) defines one corner of the slice and
        (k,l) the other slice.  As you would expect, for slice assignments,
        the argument item must of type BitArray2D.  For index-based
        assignment, the pos consists of the tuple (i,j), the point in the
        array where you want to change the value.  Again, for index-based
        assignment, the last argument will either be 1 or 0.
        '''      
        if (not isinstance( item, BitArray2D )):                     #(E2)
            if isinstance( pos, slice ):                             #(E3)
                raise ValueError("Second arg wrong for assignment")  #(E4)
            i,j = pos                                                #(E5)
            self.rowVectors[i][j] = item                             #(E6)
        # The following section is for slice assignment:
        if isinstance(pos,slice):                                    #(E7)
            if (not isinstance( item, BitArray2D )):                 #(E8)
                raise TypeError('For slice assignment, \
                        the right hand side must be a BitArray2D')   #(E9)
            arg1, arg2 = pos.start, pos.stop                        #(E10)
            i,j = ungodel(arg1)                                     #(E11)
            k,l = ungodel(arg2)                                     #(E12)
            for m in range(i,j):                                    #(E13)
                self.rowVectors[m][k:l] = item.rowVectors[m-i]      #(E14)

    def __getslice__(self, arg1, arg2):                              #(F1)
        '''
        A slice of a 2D array is defined as a rectangular region whose one
        corner is at the (i,j) coordinates, which is represented by the
        mapped integer arg1 produced by calling godel(i,j). The other
        corner of the slice is at the coordinates (k,l) that is represented
        by the integer arg2 produced by calling godel(k,l).  The slice is
        returned as a new BitArray2D instance.
        '''
        i,j = ungodel(arg1)                                          #(F2)
        k,l = ungodel(arg2)                                          #(F3)
        sliceArray = BitArray2D( rows=0, columns=0 )                 #(F4)
        if j > self.rows: j = self.rows                              #(F5)
        if l > self.columns: l = self.columns                        #(F6)
        for x in range(i,k):                                         #(F7)
            bv = self.rowVectors[x]                                  #(F8)
            sliceArray._add_row( bv[j:l] )                           #(F9)
        return sliceArray                                           #(F10)

    def __eq__(self, other):                                         #(G1)
        if self.size() != other.size(): return False                 #(G2)   
        if self.rowVectors != other.rowVectors: return False         #(G3)
        return True                                                  #(G4)

    def __ne__(self, other):                                         #(H1)
        return not self == other                                     #(H2)

    def __and__(self, other):                                        #(I1)
        '''
        Take a bitwise 'AND' of the bit array on which the method is
        invoked with the argument bit array.  Return the result as a new
        bit array.
        '''      
        if self.rows != other.rows or self.columns != other.columns: #(I2)
            raise ValueError("Arguments to AND must be of same size")#(I3)
        resultArray = BitArray2D(rows=0,columns=0)                   #(I4)
        list(map(resultArray._add_row, \
                       [self.rowVectors[i] & other.rowVectors[i] \
                                     for i in range(self.rows)]))    #(I5)
        return resultArray                                           #(I6)

    def __or__(self, other):                                         #(J1)
        '''
        Take a bitwise 'OR' of the bit array on which the method is
        invoked with the argument bit array.  Return the result as a new
        bit array.
        '''
        if self.rows != other.rows or self.columns != other.columns: #(J2)
            raise ValueError("Arguments to OR must be of same size") #(J3)
        resultArray = BitArray2D(rows=0,columns=0)                   #(J4)
        list(map(resultArray._add_row, \
                        [self.rowVectors[i] | other.rowVectors[i] \
                                    for i in range(self.rows)]))     #(J5)
        return resultArray

    def __xor__(self, other):                                        #(K1)
        '''
        Take a bitwise 'XOR' of the bit array on which the method is
        invoked with the argument bit array.  Return the result as a new
        bit array.
        '''
        if self.rows != other.rows or self.columns != other.columns: #(K2)
            raise ValueError("Arguments to XOR must be of same size")#(K3)
        resultArray = BitArray2D(rows=0,columns=0)                   #(K4)
        list(map(resultArray._add_row, \
                     [self.rowVectors[i] ^ other.rowVectors[i] \
                                   for i in range(self.rows)]))      #(K5)
        return resultArray                                           #(K6)

    def __invert__(self):                                            #(L1)
        '''
        Invert the bits in the bit array on which the method is invoked
        and return the result as a new bit array.
        '''
        resultArray = BitArray2D(rows=0,columns=0)                   #(L2)
        list(map(resultArray._add_row, [~self.rowVectors[i] \
                                   for i in range(self.rows)]))      #(L3)
        return resultArray                                           #(L4)

    def deep_copy(self):                                             #(M1)
        'Make a deep copy of a bit array' 
        resultArray = BitArray2D(rows=0,columns=0)                   #(M2)
        list(map(resultArray._add_row, [x.deep_copy() \
                                    for x in self.rowVectors]))      #(M3)
        return resultArray                                           #(M4)

    def size(self):                                                  #(N1)
        return self.rows, self.columns                               #(N2)

    def read_bit_array_from_char_file(self):                         #(P1)
        '''
        This assumes that the bit array is stored in the form of
        ASCII characters 1 and 0 in a text file. We further assume
        that the different rows are separated by the newline character.
        '''
        error_str = "You need to first construct a BitArray2D" + \
                          "instance with a filename as argument"     #(P2)  
        if not self.FILEIN:                                          #(P3)
            raise SyntaxError( error_str )                           #(P4)
        allbits = self.FILEIN.read()                                 #(P5)



        rows = filter( None, re.split('\n', allbits) )               #(P6)
        list(map(self._add_row, [BitVector.BitVector( bitstring = x ) \
                                        for x in rows]))             #(P7)

    def write_bit_array_to_char_file(self, file_out):                #(Q1)
        '''
        Note that this write function for depositing a bit array into
        text file uses the newline as the row delimiter.
        '''
        FILEOUT = open( file_out, 'w' )                              #(Q2)
        for bitvec in self.rowVectors:                               #(Q3)
            FILEOUT.write( str(bitvec) + "\n" )                      #(Q4)
             
    def read_bit_array_from_binary_file(self, rows, columns):        #(R1)
        '''
        This assumes that the bit array is stored in the form of ASCII
        characters 1 and 0 in a text file. We further assume that the
        different rows are separated by the newline character.
        '''
        error_str = "You need to first construct a BitArray2D" + \
                          "instance with a filename as argument"     #(R2)  
        if not self.filename:                                        #(R3)
            raise SyntaxError( error_str )                           #(R4)
        import os.path                                               #(R5)
        filesize = os.path.getsize( self.filename )                  #(R6)
        if (rows * columns) % 8 != 0:                                #(R7)
            raise ValueError("In binary file input mode, rows*cols must" \
                             + " be a multiple of 8" )               #(R8)
        if filesize < int(rows*columns/8):                           #(R9)
            raise ValueError("File has insufficient bytes" )        #(R10)
        bitstring = ''                                              #(R11)
        i = 0                                                       #(R12)
        while i < rows*columns/8:                                   #(R13)
            i += 1                                                  #(R14)
            byte = self.FILEIN.read(1)                              #(R15)
            hexvalue = hex( ord( byte ) )                           #(R16)
            hexvalue = hexvalue[2:]                                 #(R17)
            if len( hexvalue ) == 1:                                #(R18)
                hexvalue = '0' + hexvalue                           #(R19)
            bitstring += BitVector._hexdict[ hexvalue[0] ]          #(R20)
            bitstring += BitVector._hexdict[ hexvalue[1] ]          #(R21)
        
        bv = BitVector.BitVector( bitstring = bitstring )           #(R22)
        list(map(self._add_row, [ bv[m*columns : m*columns+columns] \
                                     for m in range(rows) ]))       #(R23)

    def write_bit_array_to_packed_binary_file(self, file_out):       #(S1)
        '''
        This creates a packed disk storage for your bit array.  But for
        this to work, the total number of bits in your bit array must be a
        multiple of 8 since all file I/O is byte oriented.  Also note that
        now you cannot use any byte as a row delimiter.  So when reading
        such a file back into a bit array, you have to tell the read
        function how many rows and columns to create.
        '''
        err_str = '''Only a bit array whose total number of bits
            is a multiple of 8 can be written to a file.'''          #(S2)
        if self.rows * self.columns % 8:                             #(S3)
            raise ValueError( err_str )                              #(S4)
        FILEOUT = open( file_out, 'wb' )                             #(S5)
        bitstring = ''                                               #(S6)
        for bitvec in self.rowVectors:                               #(S7)
            bitstring += str(bitvec)                                 #(S8)
        compositeBitVec = BitVector.BitVector(bitstring = bitstring) #(S9)
        compositeBitVec.write_to_file( FILEOUT )                    #(S10)

    def shift( self, rowshift, colshift ):                           #(T1)
        '''
        What may make this method confusing at the beginning is the
        orientation of the positive row direction and the positive 
        column direction.  The origin of the array is at the upper
        left hand corner of your display.  Rows are positive going 
        downwards and columns are positive going rightwards:
 
                       X----->  +ve col direction
                       |
                       |
                       |
                       V
                  +ve row direction

        So a positive value for rowshift will shift the array downwards
        and a positive value for colshift will shift it rightwards.
        Just remember that if you want the shifts to seem more intuitive,
        use negative values for the rowshift argument.
        '''
        if rowshift >= 0:                                            #(T2)
            self.rowVectors[rowshift : self.rows] = \
                        self.rowVectors[: self.rows-rowshift]        #(T3)
            self.rowVectors[:rowshift] = \
                    [BitVector.BitVector(size = self.columns) \
                                         for i in range(rowshift)]   #(T4)
            if colshift >= 0:     
                for bitvec in self.rowVectors[:]: \
                                     bitvec.shift_right(colshift)    #(T5)
            else:
                for bitvec in self.rowVectors[:]:                    #(T6)
                    bitvec.shift_left(abs(colshift))                 #(T7)
        else:                                                        #(T8)
            rowshift = abs(rowshift)                                 #(T9)
            self.rowVectors[:self.rows-rowshift] = \
                          self.rowVectors[rowshift : self.rows]     #(T10)
            self.rowVectors[self.rows-rowshift:] = \
                    [BitVector.BitVector(size = self.columns) \
                                         for i in range(rowshift)]  #(T11)
            if colshift >= 0:     
                for bitvec in self.rowVectors[:]: \
                               bitvec.shift_right(colshift)         #(T12)
            else:                                                   #(T13)
                for bitvec in self.rowVectors[:]:                   #(T14)
                    bitvec.shift_left(abs(colshift))                #(T15)
        return self                                                 #(T16)
    
    def dilate( self, m ):                                           #(U1)
        accumArray = BitArray2D(rows=self.rows, columns=self.columns)#(U2)
        for i in range(-m,m+1):                                      #(U3)
            for j in range(-m,m+1):                                  #(U4)
                temp = self.deep_copy()                              #(U5)
                accumArray |=  temp.shift(i,j)                       #(U6)
        return accumArray                                            #(U7)

    def erode( self, m ):                                            #(V1)
        accumArray = BitArray2D(rows=self.rows, columns=self.columns)#(V2)
        for i in range(-m,m+1):                                      #(V3)
            for j in range(-m,m+1):                                  #(V4)
                temp = self.deep_copy()                              #(V5)
                accumArray &=  temp.shift(i,j)                       #(V6)
        return accumArray                                            #(V7)
     
#------------------------  End of Class Definition -----------------------

#--------------------------- Ancillary Functions  ------------------------

def godel(i,j):                                                      #(W1)
    return 2**i*(2*j + 1)-1                                          #(W2)

def ungodel(m):                                                      #(X1)
    i,q = 0,m+1                                                      #(X2)
    while not q&1:                                                   #(X3)
        q >>= 1                                                      #(X4)
        i += 1                                                       #(X5)
    j = ((m+1)/2**i - 1)/2                                           #(X6)
    return int(i),int(j)                                             #(X7)

#------------------------     Test Code Follows    -----------------------

if __name__ == '__main__':

    print("\nConstructing an empty 2D bit array:")
    ba = BitArray2D( rows=0, columns=0 )
    print(ba)

    print("\nConstructing a bit array of size 10x10 with zero bits -- ba:")
    ba = BitArray2D( rows = 10, columns = 10 )
    print(ba)


    print("\nConstructing a bit array from a bit string -- ba2:")
    ba2 = BitArray2D( bitstring = "111\n110\n111" )
    print(ba2)                    

    print("\nPrint a specific bit in the array -- bit at 1,2 in ba2:")
    print( ba2[ godel(1,2) ] )

    print("\nSet a specific bit in the array --- set bit (0,1) of ba2:")   
    ba2[0,1] = 0
    print(ba2)

    print("\nExperiments in slice getting and setting:")
    print("Printing an array -- ba3:")
    ba3 = BitArray2D( bitstring = "111111\n110111\n111111\n111111\n111111\n111111" )
    print(ba3)
    ba4 = ba3[godel(2,3) : godel(4,5)]
    print("Printing a slice of the larger array -- slice b4 of ba3:")
    print(ba4)
    ba5 = BitArray2D( rows = 5, columns = 5 )
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
    ba8 = BitArray2D( filename = "Examples/data.txt" )
    ba8.read_bit_array_from_char_file()
    print("The bit array as read from the file -- ba8:")
    print(ba8)

    print("\nConstruct bit array from a packed binary file:")
    ba9 = BitArray2D( filename = "Examples/data_binary.dat" )
    ba9.read_bit_array_from_binary_file(rows = 5, columns = 8)
    print("The bit array as read from the file -- ba9:")
    print("size of ba9: " + str(ba9.size()))
    print(ba9)

    print("\nTest the equality and inequality operators:")
    ba10 = BitArray2D( bitstring = "111\n110" )
    ba11 = BitArray2D( bitstring = "111\n110" )
    print("ba10 is equal to ba11 is: " + str(ba10 == ba11))
    ba12 = BitArray2D( bitstring = "111\n111" )
    print("ba10 is equal to ba12 is: " + str(ba10 == ba12))

    print("\nTest shifting a bit array:")
    print("printing ba13:")
    ba13 = ba9.deep_copy()
    print(ba13)
    ba13.shift(rowshift=-2, colshift=2)
    print("The shifted version of ba9:")
    print(ba13)

    print("\nTest dilation:")
    ba14 = BitArray2D( filename = "Examples/data2.txt" )
    ba14.read_bit_array_from_char_file()
    print("Array before dilation:")
    print(ba14)
    ba15= ba14.dilate(1)
    print("Array after dilation:")
    print(ba15)

    print("\nTest erosion:")
    ba16 = BitArray2D( filename = "Examples/data2.txt" )
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

