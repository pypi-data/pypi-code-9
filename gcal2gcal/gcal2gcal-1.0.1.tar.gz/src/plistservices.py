#! /usr/bin/env python
#
#
# Copyright (c) 2003, Sarwat Khan. All rights reserved.
# 
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are
# met:
#         
#     1. Redistributions of source code must retain the above copyright
#        notice, this list of conditions and the following disclaimer.
#         
#     2. Redistributions in binary form must reproduce the above
#        copyright notice, this list of conditions and the following disclaimer
#        in the documentation and/or other materials provided with the
#        distribution.
#         
#     3. Neither Sarwat Khan's name nor the names of any contributors to
#        the plistservices software may be used to endorse or promote
#        products derived from this software without specific prior written
#        permission.
# 
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
# A PARTICULAR PURPOSE ARE DISCLAIMED.  IN NO EVENT SHALL THE COPYRIGHT
# OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
# SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
# LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
# DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
# THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#
#	plistservices
#
#		- Data
#			+ dataWithString
#			+ dataWithContentsOfFile
#			+ dataWithOpenFile
#
#		- TimeInterval (datetime.timedelta)
#			- (float) duration # seconds
#			+ durationForTimeDelta:timedelta
#			+ timeIntervalWithTimeDelta:timedelta
#
#		- Date (datetime.datetime)
#			+ dateFromStandard8601String:str
#			+ dateWithTimeIntervalSinceReferenceDate:timedelta
#			- (TimeInterval) timeIntervalSinceReferenceDate 
#			+ dateWithTimeIntervalSince1970:timedelta
#			- (TimeInterval) timeIntervalSince1970
#
#		- (object) propertyListFromData:(Data)
#		- (Data) dataFromPropertyList:(object)
#
"""Reads and writes CoreFoundation XML property list files (.plist files).
It's capable of reading any kind of plist content, not just dictionary plists.

Dates returned are datetime.datetime instances, which means it requires
Python 2.3.

Date and Data classes offer some of the functionality of their Cocoa counterparts.
"""

copyright = "Copyright (c) 2003, Sarwat Khan. All rights reserved."

import datetime
import base64, xml.sax.saxutils, warnings
import xml.parsers.expat

class Data (object):
	"""Wrapper for a generic data object.
	
	Concrete subclasses must implement bytes() to return the data bytes as a str,
	and __len__ to return the length of the data."""
	
	def dataWithString(self, string):
		"string may be unicode"
		
		return StringData(string)
	
	def dataWithContentsOfFile(self, path):
		return FileData(path)
	
	def dataWithOpenFile(self, openFile, path=None):
		return FileData(path, openFile=openFile)

	
	def __init__(self):
		raise NotImplementedError("Instantiate a subclass directly or use one of the class methods.")
	
	def stringRepForBytes(self, bytes, space32bits=False):
		# [class method]
		"converts bytes into hex, optionally putting \n"\
		"a space after every 4."
		
		result, index, length = "", 0, len(bytes)
		
		while index + 4 <= length:
			foo = bytes[index:index+4]
			result += "%02x%02x%02x%02x" % tuple([ord(x) for x in foo])
			index += 4
			
			if index < length and space32bits: result += ' '
		
		while index < length: 
			result += "%02x" % ord(bytes[index])
			index += 1
		
		return result
	
	def __str__(self):
		"same as description(), but shortened if the data if bigger than 96 bytes."
		
		result = "<"
		length = len(self)
		bytes = self.bytes()
		
		if length > 96:
			result += self.stringRepForBytes(bytes[:16], True)
			result += " ... "
			result += self.stringRepForBytes(bytes[-8:], True)
		else:
			result += self.stringRepForBytes(bytes, True)
			
		return result + ">"
	
	def description(self):
		"A Cocoa old-style plist description. I think. Unlike __str__,\n"\
		"this will return all of the data."

		return "<" + self.stringRepForBytes(self.bytes(), True) + ">"
	
	__repr__ = description
		
	def cfDescription(self):
		"A CoreFoundation-style description (CFShow, CFCopyDescription)"
		
		length = len(self)
		bytes = self.bytes()
		
		result = "<%s 0x%x>{length = %s, bytes = 0x" % (self.__class__.__name__, id(self), length)
		
		if length > 24:
			result += self.stringRepForBytes(bytes[:16])
			result += " ... "
			result += self.stringRepForBytes(bytes[-8:])
		else:
			result += self.stringRepForBytes(bytes)

		return result + "}"
	
	def bytes(self):
		"Returns the bytes of the object as a str"
		raise NotImplementedError
	
	def writeToFile(self, path):
		"Writes to the file specified by the str at path."
		
		data = self.bytes()
		
		fire = file(path, 'w')
		try:
			fire.write(data)
		finally:
			fire.close()

	dataWithString = classmethod(dataWithString)
	dataWithContentsOfFile = classmethod(dataWithContentsOfFile)
	dataWithOpenFile = classmethod(dataWithOpenFile)
	stringRepForBytes = classmethod(stringRepForBytes)
		
	
class StringData (Data):
	def __init__(self, string):
		self._value = string
	
	def __len__(self):
		return len(self. _value)
	
	def bytes(self):
		return self._value
	
class FileData (Data):
	
	def __init__(self, path, openFile=None):
		self._path = path
		
		if not openFile: self._file = file(path)
		else: self._file = openFile
	
	def __len__(self):
		saved = self._file.tell()
		self._file.seek(0, 2) # 2 == seek from end
		result = self._file.tell()
		self._file.seek(saved)
		
		return result

	def bytes(self):
		self._file.seek(0)
		return self._file.read()

# The next two classes were taken from Python 2.3 documentation
class UTCTimeZone (datetime.tzinfo):
	
	def utcoffset(self, dt): 	return datetime.timedelta(0)
	def dst(self, blah): 		return datetime.timedelta(0)
	def tzname(self, dt): 		return 'UTC'

class EasternTimeZone (datetime.tzinfo):
	"Fixed offset in minutes east from UTC."
	
	def _tzname(self, dt): 			return self.__name
	def utcoffset(self, dt): 		return self.__offset
	def dst(self, dt): 		 		return datetime.timedelta(0)	
	
	def __init__(self, offset, name=None):
		self.__offset = datetime.timedelta(minutes = offset)
		if name:
			self.__name = name
			self.tzname = self._tzname

class TimeInterval (datetime.timedelta):
	"Adds the ability to easily determine the number of seconds a \n"\
	"time delta duration represents."
	
	def duration(self):
		"Returns the duration in seconds that self represents."
		
		return self.days * 86400.0 + self.seconds + self.microseconds / 1000000.0
	
	def durationForTimeDelta(self, foo):
		# [class method]
		"Returns total seconds any timedelta object represents."
		
		return foo.days * 86400.0 + foo.seconds + foo.microseconds / 1000000.0
	
	def timeIntervalWithTimeDelta(self, belta):
		"Returns a TimeInterval object from a timedelta object."
		
		#belta was an old joke but I forgot what it was for.
		return TimeInterval(seconds=belta.seconds, 
							microseconds=belta.microseconds, 
							days=belta.days)
	
	durationForTimeDelta = classmethod(durationForTimeDelta)
	timeIntervalWithTimeDelta = classmethod(timeIntervalWithTimeDelta)
	
	
class Date (datetime.datetime):
	"Most importantly, adds dateFromStandard8601String.\nOtherwise acts a bit like NSDate."

	def dateFromStandard8601String(self, string, ignoreTimeZones=False):
		# [class method]
		"""Given an iso 8601 string, returns a datetime object.
		
		See http://www.w3.org/TR/NOTE-datetime for details. Note that
		YYYY, YYYY-MM, YYYY-MM-DD, and YYYY-MM-DDT<time> are valid.
		
		Time zone are given as Z for UTC or as an offset from UTC.
		If a time zone is not given the time interpreted in the local
		time zone."""
			
		## implementation interpreted from http://www.w3.org/TR/NOTE-datetime
		##
		result = None
		
		try:
			# try getting year. 
			year = int(string[:4])
			result = Date(year, 1, 1)
			
			# try getting the month
			if not string[4] == '-': raise SyntaxError
			month = int(string[5:7])
			result = Date(year, month, 1)
			
			# day
			if not string[7] == '-': raise SyntaxError
			day = int(string[8:10])
			result = Date(year, month, day)
			
			
			# time. Thh:mmTZD (19:20+01:00) or Thh:mm:ssTZD
			if not string[10] == 'T': raise SyntaxError
			timeStuff = string[11:]
	
			# sort time and time zone data
			#
			
				# default is local time zone.
			timeInfo, timeZone = timeStuff, None
			
			if timeStuff.rfind('Z') >= 0:
				# utc
				timeInfo , zoneInfo = timeStuff.split('Z')
				zoneInfo = "" # make sure. 
				
			elif timeStuff.rfind('+') >= 0:
				# eastern
				timeInfo, zoneInfo = timeStuff.split('+')
				zoneInfo = [zoneInfo, 1]
				
			elif timeStuff.rfind('-') >= 0:
				# western
				timeInfo, zoneInfo = timeStuff.split('-')
				zoneInfo = [zoneInfo, -1]
				
			#define the time, with zero seconds if needed.
			hms = timeInfo.split(':')
			if len(hms) == 2: 
				hours, minutes, seconds, micro = int(hms[0]), int(hms[1]), 0, 0

			else: 
				#possibly has micro seconds. grrr.
				hours, minutes, seconds_stuff = int(hms[0]), int(hms[1]), hms[2]
				if '.' in seconds_stuff:
					seconds, micro_stuff = seconds_stuff.split('.')
					seconds = int(seconds)
					
					#seconds.variable_decimal_fraction
					if len(micro_stuff) > 6: micro_stuff = micro_stuff[:6]
					exponent = 6 - len(micro_stuff)
					micro = int(micro_stuff) * 10**(exponent)
				else:
					seconds, micro = int(seconds_stuff), 0
								
			#make the time zone if needed
			if zoneInfo and not ignoreTimeZones:
				if len(zoneInfo) > 0:
					zoneoffset, zonesign = zoneInfo
					zhours, zminutes = zoneoffset.split(':')
					totalMinutes = int(zhours) * 60 + int(zminutes)
					
					# mental note. -hour == 'behind' == 'west' of utc
					timeZone = EasternTimeZone(totalMinutes * zonesign)
					
				else:
					timeZone = UTCTimeZone()
			
			result = Date(year, month, day, 
				hours, minutes, seconds, micro, timeZone)

		except:
			pass #exceptions. gotos for the 21st century.
		
		return result
	
	def dateWithDateTime(self, foo):
		# [class method] 
		"Returns a Date, not a datetime.date."
		
		return Date(foo.year, foo.month, foo.day, foo.hour, foo.minute, 
			foo.second, foo.microsecond, foo.tzinfo)
	
	def dateWithTimeIntervalSinceReferenceDate(self, belta):
		# [class method]
		"The reference date is 2001/1/1. belta may be a timedelta."
		return datetime.datetime(2001, 1, 1) + belta
	
	def timeIntervalSinceReferenceDate(self):
		"Returns a TimeInterval."
		result = datetime.datetime(2001, 1, 1) - datetime.datetime.now()
		return TimeInterval.timeIntervalWithTimeDelta(result)

	def dateWithTimeIntervalSince1970(self, belta):
		# [class method]
		"belta may be a timedelta."
		return datetime.datetime(1970, 1, 1) + belta
	
	def timeIntervalSince1970(self):
		"Returns a TimeInterval."
		result = datetime.datetime(1970, 1, 1) - datetime.datetime.now()
		return TimeInterval.timeIntervalWithTimeDelta(result)

	dateWithDateTime = classmethod(dateWithDateTime)
	dateWithTimeIntervalSinceReferenceDate = classmethod(dateWithTimeIntervalSinceReferenceDate)
	dateWithTimeIntervalSince1970 = classmethod(dateWithTimeIntervalSince1970)
	dateFromStandard8601String = classmethod(dateFromStandard8601String)

def propertyListFromData(data, noisyErrors=False):
	"""Returns a property list object from the given data, or None
	if the data was not a valid property list. 
	
	If noisyErrors is true, the exception causing the problem will
	be raised instead of None being returned. Otherwise error information
	will be 'dumped' with a UserWarning via the warnings module.
	
	Deserialized arrays are always lists (not tuples). All strings
	and dictionary keys are unicode.
	
	FYI, dictionary keys are actualy a subclass of unicode.
	
	Based on the parser from plistlib in Python 2.3."""
	
	class PlistParser (object):	
		# Not entirely robost with error handling. For example,
		# <plist><array><foo/></array></plist> is considered valid; foo is ignored.
	
		class Key(unicode):
			def __init__(self, value):
				self = value
				
		def __init__(self):
			self._parser = xml.parsers.expat.ParserCreate()
			self._parser.StartElementHandler = self._handle_begin_element
			self._parser.EndElementHandler = self._handle_end_element
			self._parser.CharacterDataHandler = self._handle_cdata
		
			self._plist = None
			self._cdata = None
			self._stack = None
			self._current = None
			
		def parse(self, data):
			self._plist = None
			
			self._parser.Parse(data.bytes(), True)
			
			if self._plist is None:
				# plist was an array or dict
				self._plist = self._stack[0]
			
			return self._plist
		
		def _handle_begin_element(self, element, attrs):
			self._cdata = None
			
			handler = getattr(self, "_begin_" + element, None)
			
			if handler: handler(attrs)
			elif element == 'plist': self._stack = []
		
		def _handle_end_element(self, element):

			handler = getattr(self, "_end_" + element, None)
			if handler: 
				self._combine_cdata()
				self._store(handler())
		
		def _handle_cdata(self, in_cdata):
			# reset after getting data after an end tag
			if type(self._cdata) is not list:
				self._cdata = []
			self._cdata.append(in_cdata)
	
		def _combine_cdata(self):
			if self._cdata:
				cdata = "".join(self._cdata)
			else:
				cdata = ""
			
			self._cdata = cdata
			#try: cdata = cdata.encode("ascii")
			#except UnicodeError: pass
			#	It should be properly encoded xml
					
		def _store(self, item):

			# handle item == key or item needs to be stored into a dictionary
			if self._stack is not None and len(self._stack) > 0:

				if isinstance(item, self.Key):
					self._stack.append(item)
				elif isinstance(self._stack[-1], self.Key):
					key = self._stack.pop()
					self._stack[-1][key] = item
			
				#if the last item on the stack is an array, we add to it
				elif isinstance(self._stack[-1], list):
					self._stack[-1].append(item)

			else:
				self._plist = item
							
		def _begin_dict(self, attribs):
			self._stack.append({})
		
		def _begin_array(self, attribs):
			self._stack.append([])
		
		def _end_dict(self):
			return self._stack.pop()

		def _end_array(self):
			return self._stack.pop()
		
		def _end_key(self):
			return self.Key(self._cdata)
			
		def _end_true(self):
			return True
			
		def _end_false(self):
			return False
			
		def _end_integer(self):
			return int(self._cdata)
			
		def _end_real(self):
			return float(self._cdata)
			
		def _end_string(self):
			return unicode(self._cdata)
			
		def _end_data(self):
			return DataString(base64.decodestring(self._cdata))
			
		def _end_date(self):
			#CFDate doesn't support time zones.
			return Date.dateFromStandard8601String(self._cdata, ignoreTimeZones=True)
	
	result = None
	parser = PlistParser()
	
	if not noisyErrors:
		try:	
			result = parser.parse(data)
		except:
			import traceback, sys

			message = "Exception parsing property list\n"
			message += "\n".join(traceback.format_exception(*sys.exc_info()))
			warnings.warn(message, UserWarning)
	else:
		result = parser.parse(data)
		
	return result
	
def dataFromPropertyList(plistSource):
	def PlistXMLWithObject(obj):
		
		def object_to_plist_xml(pyObject):
			result = ""

			if isinstance(pyObject, dict):
				result = dict_to_plist_xml(pyObject)
				
			elif isinstance(pyObject, list) or isinstance(pyObject, tuple):
				result = seq_to_plist_xml(pyObject)

			elif isinstance(pyObject, bool):
				if pyObject:
					result = "<true/>"
				else:
					result = "<false/>"
			
			elif isinstance(pyObject, long) or isinstance(pyObject, int):
				result = "<integer>%d</integer>" % pyObject
			
			elif isinstance(pyObject, float):
				result = "<real>%s</real>" % pyObject
				
			elif isinstance(pyObject, datetime.datetime):
				if pyObject.tzinfo:
					# ummmmmm
					pyObject = pyObject.tzinfo.fromutc(pyObject).replace(tzinfo=None)
				result = "<date>%s</date>" % pyObject.isoformat()
			
			elif isinstance(pyObject, Data):
				result = "<data>\n%s</data>" % base64.encodestring(pyObject.bytes())
			
			else:
				if not isinstance(pyObject, basestring):
					warnings.warn("plist.dataFromPropertyList encoding %s as string"
						% str(glass), RuntimeWarning)
				try:
					result = u"<string>%s</string>" % xml.sax.saxutils.escape(unicode(pyObject))
				except:
					result = "<string>%s</string>" % xml.sax.saxutils.escape(str(pyObject))
		
			return result
		
		def seq_to_plist_xml(pySeq):
			result = "<array/>"
			
			count = len(pySeq)
			if count:
				newline = ""
				if count > 1: newline = "\n"
				
				result = "<array>" + newline
				
				for value in pySeq:
					result = result + object_to_plist_xml(value) + newline
				
				result = result + "</array>" + newline
			
			return result
		
		def dict_to_plist_xml(pyDict):
			result = "<dict/>"
		
			count = len(pyDict)
			
			if count:
				newline = ""
				if count > 1: newline = "\n"
				
				result = "<dict>" + newline
		
				for key in pyDict.keys():
					value = pyDict[key]
					
					# +++ should post a warning if key is not str or unicode
					plistKey = u"<key>%s</key>" % key + newline
					plistValue = object_to_plist_xml(value) + newline
					
				
					result = result + plistKey + plistValue
				
				result = result + "</dict>" + newline
			
			return result
		
		result = u"""<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple Computer//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">\n"""
		
		result = result + object_to_plist_xml(obj) + "\n"
		result = result + "</plist>\n"
	
		return result.encode('utf-8')
	
	return StringData(PlistXMLWithObject(plistSource))


## initialization.
warnings.filterwarnings("always", category=UserWarning, module='plistservices')
#	 this is for parsing bad data as plists.
	
warnings.filterwarnings("always", category=RuntimeWarning, module='plistservices')
#	 this is for encoding non-plist objects as strings
