import os
import argparse
import sys
import re

def ignore(target_file, ignore_file):
	"""
	Adds the provided absolute path to .git/info/exclude so it is ignored by git.
	"""
	f = open(ignore_file, 'a')
	f.write("\n" + target_file)
	f.close()

def find_git_repo_base(working_dir):
	"""
	Figure out the base of the repo from the current working directory (i.e. where .git is).
	"""
	components = re.split("/", working_dir)

	# Get all the parent directories to search for .git in
	names = []
	for i, d in enumerate(components):
		names.append('/'.join(components[:i+1]))
	names = list(reversed(names))

	base_dir = ""
	# Go through them one by one and search
	for directory in names:
		if directory == '':
			continue
		files = os.listdir(directory)
		for f in files:
			if f == ".git":
				base_dir = directory
				break
		if base_dir != "":
			break

	if base_dir == "":
		print("Couldn't find a Git repo. :(")
		sys.exit(1)
	return base_dir