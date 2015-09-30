class tiny(object):
	'''
	Tiny is a Variable interpolator for Python string types and etc.
	You can Execute any string with Prefix '$'
	EG:
		from tiny.tiny import tiny
		name = 'Rahul'
		age	 = '18'
		gender = 'male'
		hello = 'Hi, How are you?'
		print tiny("$hello His name is $name, age is $age and is a $gender, he would like to work with you.")
		>>> Hi, How are you? His name is Rahul, age is 18 and is a male, he would like to work with you.

	This is a simple interpolation.
	For now you cannot change the interpolator, But may update that soon!
	Enjoy this for now!! :D
	'''
	import sys
	import re

	global interpolator, sys, re
	interpolator="$"

	def __init__(self, *strings):
		super(tiny, self).__init__()
		space = unicode(" ")
		self.string = space.join(strings)
		self.interpolator = interpolator
		self.__str()

	def __str(self):
		try: 1/0
		except: buffers = sys.exc_traceback.tb_frame
		while buffers.f_globals["__name__"] == __name__: buffers = buffers.f_back #Thanks to Python Itpl for this :)
		Local, Global = buffers.f_locals, buffers.f_globals

		bunGary = {}
		self.getFirms()
		for k in self.Firms:
			bunGary[str(k)] = eval(k, Local, Global)
		del self.Firms

		self.TEXER = self.__replace__(bunGary)

	def __repr__(self):
		return self.TEXER

	def __replace__(self, Dict):
		Vast = Dict
		string = self.string
		strings = string.split(" ")
		polator = self.interpolator
		for k in Vast:
			canDo = False
			repter = str(self.interpolator) + str(k)
			rapter = str(Vast[k])
			for strs in strings:
				if not str("\%s"%polator) in strs and polator in strs:
					i = strs.replace(repter, rapter)
					strings[strings.index(strs)] = i
				if str("\%s"%polator) in strs:
					i = strs.replace("\%s"%polator, "")
					strings[strings.index(strs)] = i
		del Vast

		return " ".join(strings)
	
	def getFirms(self):
		polator = self.interpolator
		self.Firms = []
		for greeker in self.string.split(" "):
			Firmates = greeker
			if not str("\%s"%polator) in Firmates and polator in Firmates:
				think = str(Firmates.split(str(polator))[1])
				a = [(s.start(0), s.end(0)) for s in re.finditer(r"[a-zA-Z0-9_]+", think)]		
				hots = False		
				if len(a) > 1:
					if think[a[0][1]] == '.'\
						and think[a[0][1]+1:] is not '':
						hots = True
				if hots:
					lenth = a[0][1]+1 + len(think[a[0][1]+1:])
					jam = str(think[a[0][0]:a[0][1]])
					thinks = think[a[0][1]+1:lenth]
					jam += '.'
					jam += str(thinks)
					think = jam
				if len(a) >= 1:
					if not hots:
						think = think[a[0][0]:a[0][1]]
				
					self.Firms.append(think)
