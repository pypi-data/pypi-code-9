import re
import subprocess
import os

def lsfiles(path, whitelist='^.*$', blacklist='^$'):
	'''
		helper function: lists all files in a directory.
	'''
	whitelist = re.compile(whitelist)
	blacklist = re.compile(blacklist)

	# List the files in natural numerical order (ascending)
	ls = subprocess.Popen(['ls', path], stdout=subprocess.PIPE)
	items = subprocess.check_output(['sort', '-n'], stdin=ls.stdout)
	ls.wait()
	items = items.split()

	# Screen out files matching blacklist or not matching whitelist
	files = [
		f for f in items
		if os.path.isfile(os.path.join(path, f))
		and whitelist.match(f) and not blacklist.match(f)
	]

	return files

