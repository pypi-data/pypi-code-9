import os
import pandas as pd

def filterList(inp,pattern,mode='include'):
	out = []
	
	#print inp, 'pattern=', pattern
	if mode =='include':
		for el in inp:
			if el.find(pattern) != -1:
				out.append(el)
	if mode == 'avoid':
		for el in inp:
			if el.find(pattern) == -1:
				out.append(el)

	return out		



def getFilelistFromDirRecursive(rootfolder, pattern):
    
    names = [os.path.join(dp, f) \
        for dp, dn, filenames in os.walk(rootfolder) \
        for f in filenames if os.path.abspath(f).find(pattern) != -1]
    
    names_new = []
    for name in names:
        names_new.append(name.replace(rootfolder,''))
    return names_new        




def getFilelistFromDir(folder,pattern,avoidpattern=None):
	"""Returns a list of files from a given source folder. 
	Filenames must match the list of patterns and must not include
	the optional list of avoidpatterns 

	:param folder: root folder where files are located
	:type folder: string
	:param pattern: string patterns. each filename in the output filename list matches all patterns 
	:param avoidpattern: string patterns. each filename in the output list does not match any of the avoidpatterns
	:type pattern: list of strings
	:type avoidpattern: list of strings
	:rtype: list of strings
	"""
	 

	allfiles = os.listdir(folder)
	selectedfiles = []

	pt = my_toList(pattern) #convert pattern string to list
	flist = allfiles	
	for patel in pt:
		flist =  filterList(flist,patel)
	

	if avoidpattern:
		av = my_toList(avoidpattern)
		for patel in av:
			flist = filterList(flist,patel,mode = 'avoid')
	return flist		


def my_toList(pattern):
	if type(pattern) is str: # if only one pattern is available
		return [pattern]
	else:
		return pattern	




def loadAndAggregate(folder,pattern,avoidpattern = None, delimiter = ',', display = True):
	"""Returns a pandas data frame aggregated from a list of spreadsheets. Spreadsheeds 
	in a given source folder are selected by matching pattern strings. 

	:param folder: root folder where files are located
	:type folder: string
	:param pattern: string patterns. each filename in the output filename list matches all patterns 
	:param avoidpattern: string patterns. each filename in the output list does not match any of the avoidpatterns
	:type pattern: list of strings
	:type avoidpattern: list of strings
	:param display: if true, progress will be logged to console 
	:rtype: pandas data frame
	"""
	
	selectedfiles = getFilelistFromDir(folder,pattern,avoidpattern)#get list of filenames filtered by pattern
	
	data = []
	i = 1.0
	for file in selectedfiles:
		if display:	
			progress = i/len(selectedfiles)*100;
			progresstr = '%.1f' % progress
			print ('loading files: '+ progresstr + '%')
		i = i+1
		table = pd.read_csv(folder+file,delimiter = delimiter)
		table['filename'] = file #the spreadsheet's filename is added as extra column
		data.append(table)
	
	return pd.concat(data)	