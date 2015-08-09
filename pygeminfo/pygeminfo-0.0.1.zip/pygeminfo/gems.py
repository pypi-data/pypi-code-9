# Importing necessary modules
import json
import sys
import collections 

try:
	import requests
except ImportError:
	print("Warning:Some functions may not work if using Python 2\n\t\tTo fix this, use 'pip install requests'")

# Imports handling
try:
	# For Python 3.0 and later
	from urllib.request import urlopen, HTTPError, URLError
except ImportError:
	# Fall back to Python 2's urllib2
	import urllib2 



#Messages to be displayed
_msg1 = "Internet connection cannot be established"
_msg2 = "Ruby gem cannot be found"
_msg3 = "Wrong Username/ID"
_msg4 = "Invalid parameters: must be 'query', | optional => page to display, amount per page |"
_msg5 = "Search parameters are 'query' | optional => page to display, amount per page "
_msg6 = "Error encountered. Try again"


# Method to open internet safely
def _readdata(link, message=_msg2):
	# Exception handling
	if sys.version < '3':
		try:
			link = urllib2.urlopen(link)
		except urllib2.HTTPError:
			sys.exit(message)
		except urllib2.URLError:
			sys.exit(_msg1)

	else:
		try:
			link = urlopen(link)
		except HTTPError:
			sys.exit(message)
		except URLError:
			sys.exit(_msg1)
			

	# Decode and convert file to JSON
	try:
		link = json.loads(link.read().decode())
		return link

	except:
		try:
			links = requests.get(link).json()
			return links
		except:
			sys.exit("Error: Use Python 3 instead. Can't retrieve info")

# Main codes

# Module Class name
class Stats:
	#initialize class variables
	def __init__(self, name):
		# Converts to lowercase
		self.gemname = name.lower()
		# Parse links
		link = 'http://rubygems.org/api/v1/gems/%s.json' %(self.gemname)

		self.data_file = _readdata(link, _msg2)


	# Class methods
	def name(self):
		#returns gem name
		return self.data_file["name"]
	
	def total(self):
		#return Gem's total downloads for all versions
		total = self.data_file["downloads"]
		return '{:3,}'.format(total)

	def latest(self):
		#returns Gem's total download for latest version 
		total = self.data_file["version_downloads"]
		return '{:3,}'.format(total)
	
	def latestversion(self):
		#returns latest version of gem 
		return self.data_file["version"]
		
	def authors(self):
		#returns gem's authors' names
		return self.data_file["authors"]
		
	def info(self):
		#returns gem's description
		return self.data_file["info"]
	
	def licenses(self):
		#returns gem's licenses
		mylist = []
		if type(self.data_file["licenses"]) == list:
			for i in self.data_file["licenses"]:
				mylist.append(str(i))
		else:
			mylist = self.data_file["licenses"]
		return mylist
	

	def metadata(self):
		#returns gem's metadata
		# If metadata is empty, return "empty metadata else return its result"
		return (self.data_file["metadata"], "empty metadata")[len(self.data_file["metadata"]) == 0]
		
	def sha(self):
		#returns gem's Secure Hash Algoruthm 256 Checksum
		return self.data_file["sha"]
	
	def gemURL(self):
		#returns gem's URL
		return self.data_file["gem_uri"]
	

	def projectURL(self):
		#returns gem's project URL
		return self.data_file["project_uri"]
	
	def homepage(self):
		#returns gem's dedicated website 
		return self.data_file["homepage_uri"]
	
	def wikiURL(self):
	#returns gem's wiki URL
		return self.data_file["wiki_uri"]
	
	def docURL(self):
		#returns gem's documentation URL
		return self.data_file["documentation_uri"]
	
	def mailURL(self):
		#returns gem's mailing list URL
		return self.data_file["mailing_list_uri"]
	
	def sourceURL(self):
		#returns gem's source-code URL
		return self.data_file["source_code_uri"]
	
	def bugURL(self):
		#returns gem's bug tracking URL
		return self.data_file["bug_tracker_uri"]
	
# Module Method names
def gemversions(gemname):
	#Converts gemname to lowercase
	gemname = gemname.lower()

	#self.gemversion = version
	#"https://rubygems.org/api/v1/downloads/eventsims-0.0.2.json"
	
	#parse links
	link = 'http://rubygems.org/api/v1/versions/' + gemname + ".json"

	data_file = _readdata(link, _msg2)

	# Printing values
	x = 0; 
	while x < len(data_file):
		print("Gem Name: {}-{}".format(gemname,data_file[x]["number"]))
		print("Authors: {}".format(data_file[x]["authors"]))
		print("Built on: {}".format(data_file[x]["built_at"][:10]))
		print("Total downloads: {}".format(data_file[x]["downloads_count"]))
		print("SHA 256 Checksum: {}\n".format(data_file[x]["sha"]))
		x+=1
	
 
#Module method
def downloads():

	link = "http://rubygems.org/api/v1/downloads.json"
	data_file = _readdata(link, _msg6)

	total = '{:3,}'.format(data_file["total"])
	print("Total Rubygems Downloads till date: {}".format(total))

def usergems(username):
	#Converts gemname to lowercase
	username = str(username.lower())
	#http://rubygems.org/api/v1/owners/tushortz/gems.json
	
	#parse links
	link = "http://rubygems.org/api/v1/owners/{}/gems.json".format(username)
	# print(link)
	data_file = _readdata(link, _msg3)
	
	# If the type of data online is a list give totalgems the value of list length
	totalgem = (0, len(data_file))[type(data_file) == list]
	
	# Checks if value can be converted to a number and assigns it to a value
	user = "User ID"
	try: int(username)
	except ValueError: user = "User Name"

	print("{}: {}".format(user, username))
	gemresult = ("No gems found", totalgem)[totalgem !=0] 
	print("Total Gems: {}\n".format(gemresult))

	titles = ["Gemname", "Overall downloads", "latest version", "Latest version downloads"]
	
	key = ["name", "downloads", "version", "version_downloads"]


	for  d in data_file:
		results = []
		for k in key:
			val = d[k]
			if isinstance(val, int):
				val = "{:,}".format(val)
			print("{}: {}".format(titles[key.index(k)], val))
		print("")

def owner(gemname):
	#Converts gemname to lowercase
	gemname = str(gemname.lower())

	#http://rubygems.org/api/v1/gems/event/owners.json
	
	#parse links
	link = "http://rubygems.org/api/v1/gems/" + gemname + "/owners.json"

	#Exception handling
	data_file = _readdata(link, _msg2)

	print("Gemname: {} \n".format(gemname))

	try:
		for x in data_file:
			print("User ID: {}".format(x["id"]))
			print("Username: {}".format(x["handle"]))
			print("Email Address: {}\n".format(x["email"]))
	except:
		pass
		
def search(query, *args):
	#Converts gemname to lowercase
	query = str(query.lower())

	if len(args) == 0:
		pageno = "1"
	elif len(args) == 1:
		pageno = str(args[0])
	elif len(args) == 2:
		pageno = str(args[0])
	else:
		sys.exit("Invalid parameters: must be 'query', | optional => page to display, amount per page |") 
	
	#http://rubygems.org/api/v1/search.json?query=d&page=1

	#parse links
	link = "https://www.rubygems.org/api/v1/search.json?query={}&page={}".format(query, pageno)
	
	#Exception handling
	data_file = _readdata(link, _msg5)

	#Variable declaration and checks
	try:
		if len(args) == 2:
			amount = int(args[1])
		else:
			amount = len(data_file)

		if amount > len(data_file): amount = len(data_file) 

		x=0;
		while x < amount:
			print("Gem Name: {}".format(data_file[x]["name"]))
			print("Author: {}".format(data_file[x]["authors"]))
			print("Latest Version: {}".format(data_file[x]["version"]))
			print("Total Downloads: {}\n".format(data_file[x]["downloads"]))
			x+=1
		
		#Show  of data
		if amount < 30: print("End of data") 
	except TypeError as e:
		#sys.exit("Invalid arguments")
		print(e)


#Module method
def latestgems(amount=50):

	link = "http://rubygems.org/api/v1/activity/latest.json"
	data_file = _readdata(link, _msg6)

	x=0; 
	while x < int(amount):
		print("Gem Name: {}".format(data_file[x]["name"]))
		print("Author: {}".format(data_file[x]["authors"]))
		print("Latest Version: {}".format(data_file[x]["version"]))
		print("Total Downloads: {:3,}".format(data_file[x]["downloads"]))
		print("Description: {}\n".format(data_file[x]["info"]))
		x+=1
	

#Module method
def updatedgems(amount=50):
	link = "http://rubygems.org/api/v1/activity/just_updated.json"
	data_file = _readdata(link, _msg6)

	x=0; 
	while x < int(amount):
		print("Gem Name: {}".format(data_file[x]["name"]))
		print("Author: {}".format(data_file[x]["authors"]))
		print("Latest Version: {}".format(data_file[x]["version"]))
		print("Total Downloads: {:3,}".format(data_file[x]["downloads"]))
		print("Description: {}\n".format(data_file[x]["info"]))
		x+=1


	


