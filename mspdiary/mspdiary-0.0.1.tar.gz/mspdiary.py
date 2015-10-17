import datetime
import os
import subprocess
import ConfigParser
import shutil


BASE_PATH = os.path.expanduser('~/.mspdiary/')

DEFAULT_CONFIG = """
[main]
# The executable to be invoked for editing the files.
text_editor=vim
"""
CONFIG_FILE_PATH = BASE_PATH + 'config.ini'
TEXT_EDITOR = None


def main():
	setup()

	today_path = BASE_PATH + today_filename()
	subprocess.call([text_editor(), today_path])

def today_filename():
	today = datetime.datetime.today()
	filename = "%s_%s_%s.txt" % (today.year, today.month, today.day)
	return filename

def text_editor():
	parser = ConfigParser.SafeConfigParser()
	parser.read(CONFIG_FILE_PATH)
	return parser.get('main', 'text_editor')

def setup():
	create_file(BASE_PATH)

	if not os.path.exists(CONFIG_FILE_PATH):
		config_file = open(CONFIG_FILE_PATH, 'w')
		config_file.write(DEFAULT_CONFIG)
		config_file.close()

def create_file(path):
	if not os.path.exists(path):
		try:
			os.makedirs(path)
		except OSError as exception:
			raise

if __name__ == '__main__':
    main()
