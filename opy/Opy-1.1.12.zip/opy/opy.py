#! /usr/bin/python

license = (
'''_opy_Copyright (C) 2015 Jacques de Hooge, Geatec Engineering, www.geatec.com

This program is free software.
You can use, redistribute and/or modify it, but only under the terms stated in the QQuickLicence.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY, without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.

See the full QualityQuick licence at www.qquick.org/licence.html for details.'''
)

import re
import os
import sys
import errno
import keyword
import importlib
import random
import codecs
import shutil

# =========== Initialize constants

programName = 'opy'
programId = '_{0}_'.format (programName)

random.seed ()

isPython2 = sys.version_info [0] == 2
stringOffset = 0
stringBase = 0
charBase = 2048
charModulus = 7

# =========== Utilities

def createFilePath (filePath, open = False, isUtf8 = False):
	try:
		os.makedirs (filePath.rsplit ('/', 1) [0])
	except OSError as exception:
		if exception.errno != errno.EEXIST:
			raise
			
	if open:
		if isUtf8:
			return codecs.open (filePath, encoding = 'utf-8', mode = 'w')
		else:
			return open (filePath, mode = 'w')
	
def getObfuscatedName (obfuscationIndex, startsWithUnderscore):
	return '{0}{1}{2}'.format ('_' if startsWithUnderscore else 'l', bin (obfuscationIndex) [2:] .replace ('0', 'l'), obfuscatedNameTail)
	
def scramble (stringLiteral):
	global isPython2
	global stringBase
	global stringOffset
	global charBase
	global charModulus
	
	if isPython2:
		stringLiteral = unicode (stringLiteral)
		
	for delimiter in ("'''", '"""', "'", '"'):
		if stringLiteral.endswith (delimiter):
			break
			
	delimiterLength = len (delimiter)
			
	startPos = stringLiteral.find (delimiter)
	string = eval (stringLiteral)	# Replace escape sequences by the chars they denote
	prefix = stringLiteral [:startPos] .lower ()
	stringNr = stringBase + stringOffset
		
	if string:
		stringShift = stringNr % len (string)
	else:
		stringShift = 0
		
	if isPython2:
		if not 'u' in prefix:
			prefix = 'u' + prefix
		string = u''.join ([unichr (ord (aChar) + charBase + (charIndex + stringNr) % charModulus) for charIndex, aChar in enumerate (string)])
		stringKey = unichr (charBase + stringNr)
	else:
		string = ''.join ([chr (ord (aChar) + charBase + (charIndex + stringNr) % charModulus) for charIndex, aChar in enumerate (string)])
		stringKey = chr (charBase + stringNr)
			
	return prefix + delimiter + string [:-stringShift] + string [-stringShift:] + stringKey + delimiter
	
def getUnScrambler (stringBase):
	return '''
import sys

isPython2{0} = sys.version_info [0] == 2
stringBase{0} = {1}
charBase{0} = {2}
charModulus{0} = {3}
asciiStrings{0} = {4}

def unScramble{0} (string{0}):
	global isPython2{0}
	global stringBase{0}
	global charBase{0}
	global charModulus{0}
	
	stringNr{0} = ord (string{0} [-1]) - charBase{0}
	string{0} = string{0} [:-1]
	
	if string{0}:
		stringShift{0} = (stringNr{0}) % len (string{0})	
	else:
		stringShift{0} = 0
	
	if isPython2{0}:
		unicodeUnscrambled{0} = u'{0}'.join ([unichr (ord (aChar{0}) - charBase{0} - (charIndex{0} + stringNr{0}) % charModulus{0}) for charIndex{0}, aChar{0} in enumerate (string{0} [:stringShift{0}] + string{0} [stringShift{0}:])])
	else:
		unicodeUnscrambled{0} =	'{0}'.join ([chr (ord (aChar{0}) - charBase{0} - (charIndex{0} + stringNr{0}) % charModulus{0}) for charIndex{0}, aChar{0} in enumerate (string{0} [:stringShift{0}] + string{0} [stringShift{0}:])])
		
	if asciiStrings{0}:
		return str (unicodeUnscrambled{0})
	else:
		return unicodeUnscrambled{0}
'''.format (programId, stringBase, charBase, charModulus, asciiStrings)	
		
def printHelpAndExit (errorLevel):
	print (r'''
	
*******************************************************************************
{0} will obfuscate your extensive, real world, multi module Python source code for free!
And YOU choose per project what to obfuscate and what not, by editting the config file.

BACKUP YOUR CODE AND VALUABLE DATA TO AN OFF-LINE MEDIUM FIRST TO PREVENT ACCIDENTAL LOSS OF WORK!!!

Then copy the default config file to the source top directory <topdir> and run {0} from there.
It will generate an obfuscation directory <topdir>/../<topdir>_{1}

At first some identifiers may be obfuscated that shouldn't be, e.g. some of those imported from external modules.	
Adapt your config file to avoid this, e.g. by adding external module names that will be recursively scanned for identifiers.
You may also exclude certain words or files in your project from obfuscation explicitly.
Source directory, obfuscation directory and config file path can also be supplied as command line parameters in that order.
Comments and string literals can be marked as plain, bypassing obfuscation

Known limitations:
A comment after a string literal should be preceded by whitespace
A ' or " inside a string literal should be escaped with \ rather then doubled
A {2} in a string literal can only be used at the start, so use 'p''{2}''r' rather than 'p{2}r'
Obfuscation of string literals is unsuitable for sensitive information since it can be trivially broken

Licence:
{3}
*******************************************************************************
	'''.format (programName.capitalize (), programName, r'#', license))
	exit (errorLevel)
	
# ============ Assign directories ============

if len (sys.argv) > 1:
	if '?' in sys.argv [1]:
		printHelpAndExit (0)
	sourceRootDirectory = sys.argv [1]
else:
	sourceRootDirectory = os.getcwd () .replace ('\\', '/')

if len (sys.argv) > 2:
	targetRootDirectory = sys.argv [2]
else:
	targetRootDirectory = '{0}/{1}_{2}'.format (* (sourceRootDirectory.rsplit ('/', 1) + [programName]))

if len (sys.argv) > 3:
	configFilePath = sys.argv [3]
else:
	configFilePath = '{0}/{1}_config.txt'.format (sourceRootDirectory, programName)

# =========== Read config file

try:
	configFile = open (configFilePath)
except Exception as exception:
	print (exception)
	printHelpAndExit (1)
	
exec (configFile.read ())
configFile.close ()

try:
	obfuscateStrings = obfuscate_strings
except:
	obfuscateStrings = False
	
try:
	asciiStrings = ascii_strings
except:
	asciiStrings = False
	
try:
	obfuscatedNameTail = obfuscated_name_tail
except:
	obfuscatedNameTail = ''
	
try:
	plainMarker = plain_marker
except:
	plainMarker = '_opy_'
	
fileNameExtensionList = source_extensions.split ()
externalModuleNameList = external_modules.split ()
plainFileRelPathList = plain_files.split ()
extraPlainWordList = plain_names.split ()

# ============ Gather source file names

sourceFilePathList = [
	'{0}/{1}'.format (directory.replace ('\\', '/'), fileName)
	for directory, subDirectories, fileNames in os.walk (sourceRootDirectory)
	for fileName in fileNames
]

# =========== Define comment swapping tools
		
shebangCommentRegEx = re.compile (r'^{0}!'.format (r'#'))
codingCommentRegEx = re.compile ('coding[:=]\s*([-\w.]+)')
keepCommentRegEx = re.compile ('.*{0}.*'.format (programId), re.DOTALL)
	
def getCommentPlaceholderAndRegister (matchObject):
	comment = matchObject.group (0)
	if keepCommentRegEx.search (comment):	# Rare, so no need for speed
		replacedComments.append (comment.replace (programId, ''))
		return commentPlaceholder
	else:
		return ''
	
def getComment (matchObject):
	global commentIndex
	commentIndex += 1
	return replacedComments [commentIndex]
	
commentRegEx = re.compile (r'{0}{1}{2}.*?$'.format (
	r"(?<!')",
	r'(?<!")',
	r'#'
), re.MULTILINE)

commentPlaceholder = '_{0}_c_'.format (programName)
commentPlaceholderRegEx = re.compile (r'{0}'.format (commentPlaceholder))

# ============ Define string swapping tools

keepStringRegEx = re.compile (r'.*{0}.*'.format (programId))
	
def getDecodedStringPlaceholderAndRegister (matchObject):
	string = matchObject.group (0)
	if obfuscateStrings:
		if keepStringRegEx.search (string):	# Rare, so no need for speed
			replacedStrings.append (string.replace (programId, ''))
			return stringPlaceholder	# Store original string minus programId, no need to unscramble
		else:
			global stringOffset
			stringOffset = random.randrange (64)
			replacedStrings.append (scramble (string))
			return 'unScramble{0} ({1})'.format (programId, stringPlaceholder)	# Store unScramble (<scrambledString>)
	else:
		replacedStrings.append (string)
		return stringPlaceholder
	
def getString (matchObject):
	global stringIndex
	stringIndex += 1
	return replacedStrings [stringIndex]

stringRegEx = re.compile (r'([ru]|ru|ur)?(({0})|({1})|({2})|({3}))'.format (
	r"'''.*?(?<![^\\]\\)(?<![^\\]\')'''",
	r'""".*?(?<![^\\]\\)(?<![^\\]\")"""',
	r"'.*?(?<![^\\]\\)'",
	r'".*?(?<![^\\]\\)"'
), re.MULTILINE | re.DOTALL | re.VERBOSE)

stringPlaceholder = '_{0}_s_'.format (programName)
stringPlaceholderRegEx = re.compile (r'{0}'.format (stringPlaceholder))

# ============ Define identifier recognition tools

identifierRegEx = re.compile (r'''
	\b			# Delimeted
	(?!__)		# Not starting with __
	(?!{0})		# Not starting with commentPlaceholder
	(?!{1})		# Not starting with stringPlaceholder
	[^\d\W]		# De Morgan: Not (decimal or nonalphanumerical) = not decimal and alphanumerical
	\w*			# Alphanumerical
	(?<!__)		# Not ending with __
	(?<!{0})	# Not ending with commentPlaceholder
	(?<!{1})	# Not ending with stringPlaceHolder
	\b			# Delimited
'''.format (commentPlaceholder, stringPlaceholder), re.VERBOSE)	# De Morgan

chrRegEx = re.compile (r'\bchr\b')

# =========== Generate skip list

skipWordSet = set (keyword.kwlist + extraPlainWordList)

for plainFileRelPath in plainFileRelPathList:
	plainFile = open ('{0}/{1}'.format (sourceRootDirectory, plainFileRelPath))
	content = plainFile.read ()
	plainFile.close ()
	
	# Throw away comment-like line tails
	
	content = commentRegEx.sub ('', content)
	
	# Throw away strings
	
	content = stringRegEx.sub ('', content)
	
	# Put identifiers in skip word set
	
	skipWordSet.update (re.findall (identifierRegEx, content))
	
class ExternalModules:
	def __init__ (self):
		for externalModuleName in externalModuleNameList:
			attributeName = externalModuleName.replace ('.', programId)	# Replace . in module name by placeholder to get attribute name
			
			try:
				exec (
					'''
import {0} as currentModule
					'''.format (externalModuleName),
					globals ()
				)
				setattr (self, attributeName, currentModule)	
			except Exception as exception:
				print (exception)
				setattr (self, attributeName, None)	# So at least the attribute name will be available
				print ('Warning: could not inspect external module {0}'.format (externalModuleName))
			
externalModules = ExternalModules ()
externalObjects = set ()
			
def addExternalNames (anObject):
	if anObject in externalObjects:
		return
	else:
		externalObjects.update ([anObject])

	try:
		attributeNameList = list (anObject.__dict__)
	except:
		attributeNameList = []
	
	try:
		if isPython2:
			parameterNameList = list (anObject.func_code.co_varnames)
		else:
			parameterNameList = list (anObject.__code__.co_varnames)
	except:		
		parameterNameList = []
		
	attributeList = [getattr (anObject, attributeName) for attributeName in attributeNameList]
	attributeSkipWordList = (programId.join (attributeNameList)) .split (programId)	# Split module name chunks that were joined by placeholder
	
	updateSet = set ([entry for entry in (parameterNameList + attributeSkipWordList) if not (entry.startswith ('__') and entry.endswith ('__'))])
	skipWordSet.update (updateSet)
	
	for attribute in attributeList:	
		try:
			addExternalNames (attribute)
		except:
			pass

addExternalNames (__builtins__)
addExternalNames (externalModules)

skipWordList = list (skipWordSet)
skipWordList.sort (key = lambda s: s.lower ())

# ============ Generate obfuscated files

obfuscatedWordList = []
obfuscatedRegExList = []

for sourceFilePath in sourceFilePathList:
	if sourceFilePath == configFilePath:	# Don't copy the config file to the target directory
		continue

	sourceDirectory, sourceFileName = sourceFilePath.rsplit ('/', 1)
	sourceFilePreName, sourceFileNameExtension = sourceFileName.rsplit ('.', 1)
	targetSubDirectory = '{0}{1}'.format (targetRootDirectory, sourceFilePath [len (sourceRootDirectory) : ]) .rsplit ('/', 1) [0]
	
	# Read plain source

	if sourceFileNameExtension in fileNameExtensionList:
		stringBase = random.randrange (64)
	
		try:
			sourceFile = codecs.open (sourceFilePath, encoding = 'utf-8')
			content = sourceFile.read ()
			sourceFile.close ()
			targetIsUtf8 = True
		except Exception as exception:
			sourceFile.close ()
			sourceFile = open (sourceFilePath)
			content = sourceFile.read ()
			sourceFile.close ()
			targetIsUtf8 = False
			
		if not targetIsUtf8:
			if isPython2:
				content = unicode (content, 'utf-8')
			targetIsUtf8 = True
		
		# Replace comment-like linetails by comment placeholders

		replacedComments = []
		contentList = content.split ('\n', 2)
			
		nrOfSpecialLines = 0
		insertCodingComment = True
		
		if len (contentList) > 0:
			if shebangCommentRegEx.search (contentList [0]):
				nrOfSpecialLines += 1
				if len (contentList) > 1 and codingCommentRegEx.search (contentList [1]):
					nrOfSpecialLines += 1
					insertCodingComment = False
			elif codingCommentRegEx.search (contentList [0]):
				nrOfSpecialLines += 1
				insertCodingComment = False
			
		if obfuscateStrings and insertCodingComment:
			contentList [nrOfSpecialLines:nrOfSpecialLines] = ['# coding: UTF-8']
			nrOfSpecialLines += 1
		
		if obfuscateStrings:
			normalContent = '\n'.join ([getUnScrambler (stringBase)] + contentList [nrOfSpecialLines:])
		else:
			normalContent = '\n'.join (contentList [nrOfSpecialLines:])
		
		normalContent = commentRegEx.sub (getCommentPlaceholderAndRegister, normalContent)
		 
		# Replace strings by string placeholders
		
		replacedStrings = []
		normalContent = stringRegEx.sub (getDecodedStringPlaceholderAndRegister, normalContent)
			
		# Obfuscate content without strings
		
		# change char in unichar if needed
		
		if obfuscateStrings and isPython2:
			normalContent = chrRegEx.sub ('unichr', normalContent)
		
		# All source words and module name
		sourceWordSet = set (re.findall (identifierRegEx, normalContent) + [sourceFilePreName])

		# Add source words that are not yet obfuscated and shouldn't be skipped to global list of obfuscated words, preserve order of what's already there
		strippedSourceWordSet = sourceWordSet.difference (obfuscatedWordList).difference (skipWordSet)
		strippedSourceWordList = list (strippedSourceWordSet)
		strippedSourceRegExList = [re.compile (r'\b{0}\b'.format (sourceWord)) for sourceWord in strippedSourceWordList]
		obfuscatedWordList += strippedSourceWordList			
		obfuscatedRegExList += strippedSourceRegExList
		
		for obfuscationIndex, obfuscatedRegEx in enumerate (obfuscatedRegExList):
			normalContent = obfuscatedRegEx.sub (getObfuscatedName (obfuscationIndex, obfuscatedWordList [obfuscationIndex] .startswith ('_')), normalContent)	# Use regex to prevent replacing word parts
			
		# Replace string placeholders by strings
		
		stringIndex = -1
		normalContent = stringPlaceholderRegEx.sub (getString, normalContent)
	
		# Replace nonempty comment placeholders by comments
		
		commentIndex = -1
		normalContent = commentPlaceholderRegEx.sub (getComment, normalContent)
		
		content = '\n'.join (contentList [:nrOfSpecialLines] + [normalContent])
		
		# Write target 
			
		try:
			targetFilePreName = getObfuscatedName (obfuscatedWordList.index (sourceFilePreName), sourceFilePreName.startswith ('_'))
		except:	# Top level module name, not in list
			targetFilePreName = sourceFilePreName
		
		targetFile = createFilePath ('{0}/{1}.{2}'.format (targetSubDirectory, targetFilePreName, sourceFileNameExtension), open = True, isUtf8 = targetIsUtf8)
		targetFile.write (content)
		targetFile.close ()
	else:
		targetFilePath = '{0}/{1}'.format (targetSubDirectory, sourceFileName)
		createFilePath (targetFilePath)
		shutil.copyfile (sourceFilePath, targetFilePath)
		
print ('Obfuscated words: {0}'.format (len (obfuscatedWordList)))

