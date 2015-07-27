'''
simple_math: some simple math functions
Copyright (C) 2015 Noah May

This program is free software; you can redistribute it and/or
modify it under the terms of the GNU General Public License
as published by the Free Software Foundation; either version 2
of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program; if not, write to the Free Software
Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.
'''

import math

def exno(num,powers=False):
	'''exno(...) --> str

	Return the Expanded Notation in a string
	optional argument powers defines the format for place value
	eg. False: 100000  True: 10^5'''
	# define function to either return or modify string
	if powers:
		func=lambda x: x
	else:
		func=lambda x: str(eval(x))
	# handle negitive values
	if num<0:
		start='-'
		num=str(float(num)).replace('-','')
	else:
		start=''
		num=str(float(num))
	# define list of significant digits
	strings=[]
	# variable to represent exponent
	exponent=num.index('.')-1
	# remove decimal point
	num=num.replace('.','')
	# iterate through num and add a str value
	# of the significant digit to "strings"
	for n in num:
		if n!='0':
			strings.append(' '.join(\
				[start+'(',n,'*',func('10**'+str(exponent)),')']\
			))
		exponent-=1
	# return results
	return ' + '.join(strings)

def factors(num):
	'''factors(...) --> list

	Return all factors of an int as a list
	Raises ValueError for negitive or
	floating point numbers'''
	# check for invalid numbers (negitive or floating point)
	if num<0 or int(num)!=num:
		raise ValueError('Invalid value: '+str(num))
	# list to hold factors
	l=[]
	# iterate through range and x is a factor
	# add x and div to l
	for x in range(1,int(math.sqrt(num))+1):
		div=num/x
		if int(div)==div:
			l.extend([x,int(div)])
	# return results
	return sorted(set(l))

def gcf(num1,num2):
	'''gcf(...) --> int

	Return the Greatest Common Factor of two numbers
	Already implemented in module "fractions" (and "math" in python 3.5)
	may remove in future'''
	if num2==0: return num1
	else: return gcf(num2,num1%num2)

def gcfl(l):
	'''gcfl(...) --> int

	Return the Greatest Common Factor of a list of numbers'''
	# if list is empty return 0
	if not l:
		return 0
	# variable for GCF
	val=l[0]
	# get GCF of list "l"
	for n in l:
		val=gcf(val,n)
	# return results
	return val

def lcd(num1,num2):
	'''lcd(...) --> int

	Return the Least Common Denominator of two numbers'''
	return int(num1*num2/gcf(num1,num2))

def lcdl(l):
	'''lcdl(...) --> int

	Return the Least Common Denominator of a list of numbers'''
	# check for invalid numbers
	if 0 in l:
		raise ValueError('invalid number "0"')
	# if list is empty return 0
	if not l:
		return 0
	# variable for GCF
	val=l[0]
	# get GCF of list "l"
	for n in l:
		val=lcd(val,n)
	# return results
	return val

def mean(l):
	'''mean(...) --> float

	Return the Mean (Average) of a list of numbers'''
	return sum(l)/len(l)

def median(l):
	'''median(...) --> float

	Return the Median of a list of numbers'''
	# sort "l"
	l.sort()
	# variable
	val=(len(l)-1)/2
	# int makes a makeshift floor function
	return (l[int(val)]+l[math.ceil(val)])/2

def mode(l):
	'''mode(...) --> list

	Return the Mode(s) in a list'''
	# sort "l"
	l.sort()
	# variable for amount of individual numbers
	amount=0
	# variable for amount of the most numbers
	main_amount=0
	# previous number
	pre_x=None
	# list of mode(s)
	modes=[]
	# iterate through "l"
	for x in l:
		# if number is same as the previous increment amount
		if x==pre_x:
			amount+=1
		# reached a new number
		else:
			pre_x=x
			amount=1
		# if the amount is equal to amount of modes x is also a mode
		if amount==main_amount:
			modes.append(x)
		# if there is more pre_x 's then any other
		# then it's the only mode
		elif amount>main_amount:
			modes=[x]
			main_amount=amount
	return modes

def pvint(num,place_value=1):
	'''pvint(...) --> int
	
	This is an old function and is replacable by plval
	Will be removed in future versions'''
	return plval(num,place_value-1)

def pvfloat(num,place_value=1.0):
	'''pvfloat(...) --> int
	
	This is an old function and is replacable by plval
	Will be removed in future versions'''
	return plval(num,int(place_value)-1)

def plval(num,place_value=0):
	'''plval(...) --> int

	Return the Place Value of a number
	Place_value refers to n where the specified digit is in the 10^n slot
	Raises ValueError if place value provided is invalid'''
	# turn num into two parts: left of and right of the decimal point
	num=str(float(num)).split('.')
	try:
		# if place value refers to the left of the decimal point
		if place_value>=0:
			return int(num[0][-(place_value+1)])
		# if not
		else:
			return int(num[1][-(place_value+1)])
	# otherwise place_value is invalid
	except IndexError:
		raise ValueError('invalid place value: '+str(place_value))

def prifac(num):
	'''prifac(...) --> list

	Return the Prime Factorization of num in a list'''
	# if number can't have prime factors
	if num<2:
		return []
	# list to hold factors
	factors=[]
	# iterate through primes up to square root of num
	for p in primes_to(math.sqrt(num)):
		# while divisable by prime add prime to factors
		# and asign num to num/p
		while num%p==0:
			factors.append(p)
			num/=p
		# if all prime factors is less then sqrt(num)
		if num==1:
			return factors
	# otherwise
	return factors+[int(num)]

def prime(num):
	'''prime(...) --> bool

	Return True if num is a prime number and False if not'''
	# if num is obviously not a prime return False
	if (num<2) | (int(num)!=num) | (num%2==0):
		return False
	# iterate through odd numbers to the square root of num
	# if num is divisible by odd return False
	for odd in range(3,int(math.sqrt(num)),2):
		if num%odd==0:
			return False
	# else return True
	return True

def primes_to(num):
	'''primes_to(...) --> list

	Return a list of all the primes up to a number'''
	# if number less then all primes
	if num<2:
		return []
	# list to hold primes
	primes=[]
	# iterate through odd numbers
	for odd in range(3,int(num+1),2):
		# iterate through primes
		for prime in primes:
			if odd%prime==0:
				break
		# if odd is prime add it to "primes"
		else:
			primes.append(odd)
	# return results
	return [2]+primes

def psr(num):
	'''psr(...) --> bool

	Return true if num has a Perfect Square Root and false otherwise'''
	sr=math.sqrt(num)
	if int(sr)==sr:
		return True
	return False

def refine(string,variables=[]):
	'''refine(...) --> str

	Return a parsed math term mostly readable by python
	eg.  .25 -> 0.25 ,  2x(54/3) -> 2*x*(54/3) ,
	 | 1-x^3 \|/{10-4} -> (abs (1-x**3) )/(10-4)  etc.
	second parameter is a list of single character
	reserved as unknown values
	Not fully reliable
	Will be changed in future versions'''
	string=string.replace(' ','')
	string=string.replace('^','**')
	string=string.replace('[','(')
	string=string.replace(']',')')
	string=string.replace('{','(')
	string=string.replace('}',')')
	string=string.replace('\|',') )')
	string=string.replace('|','(abs (')
	last_index=-1
	for _ in range(string.count('.')):
		index=string.index('.',last_index+1)
		if index!=0:
			if not string[index-1].isdigit():
				string=string[:index]+'0.'+string[index+1:]
		else:
			string='0'+string
		last_index=index
	last_index=-1
	for _ in range(string.count('(')):
		index=string.index('(',last_index+1)
		if index!=0 and (string[index-1].isdigit()\
				 or string[index-1] in variables):
			string=string[:index]+'*('+string[index+1:]
		last_index=index
	last_index=-1
	for _ in range(string.count(')')):
		length=len(string)
		index=string.index(')',last_index+1)
		if index+1<length:
			if string[index+1].isdigit()\
			   or string[index+1] in variables+['(']:
				string=string[:index]+')*'+string[index+1:]
		last_index=index
	for v in variables:
		last_index=-1
		for _ in range(string.count(v)):
			index=string.index(v,last_index+1)
			if index!=0 and string[index-1] not in '+-*/%()':
				string=string[:index]+'*'+v+string[index+1:]
			if index+1<len(string):
				if string[index+1]not in '+-*/%()'+v:
					string=string[:index]+v+\
						'*'+string[index+1:]
	return string

