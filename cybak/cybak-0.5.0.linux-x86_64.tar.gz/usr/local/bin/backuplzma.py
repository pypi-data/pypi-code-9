import sys
import os
from os import path
import re
import tarfile
import logging
import time
import random

from dirwalker.dirwalker import file_lister
import config_handler
import pash
import termcolor
import menu_generator


# decide where the configuration file should reside and look for it 
#file_name = os.path.abspath(sys.argv[0])
#dir_path = os.path.dirname(file_name)
config_path = '/etc/cybak.cfg'
config = config_handler.Parser(filename=config_path)
if config.config_exists(config_path) != True:
    print "No configuration file found. Using defaults."


# a function to build lists of exceptions from a setting
def build_exceptions(except_option):
    try:
        except_list = config.get_setting('EXCEPT',
                        except_option).split(',')
        if except_list[-1] == ['']:
            except_list.pop()
    except AttributeError:
        except_list = []
    return except_list

# build the file and directory exception lists 
dir_exceptions = build_exceptions('DIR_EXCEPT')
file_exceptions = build_exceptions('FILE_EXCEPT')


# set destination directory to default
dest_dir = '/backup/'
# change destination root if the setting is non-blank
if config.get_setting('DIR','DEST_DIR') != None:
    dest_dir = config.get_setting('DIR','DEST_DIR')

# set source directory to default
source_dir = os.environ['HOME']
# change the source root if the setting is non-blank
if config.get_setting('DIR','SRC_DIR') != None:
    source_dir = config.get_setting('DIR','SRC_DIR')

# set backup file name to default
file_handle = 'MyBackup'
# change the backup file name if the setting is non-blank
if config.get_setting('NAME','FILENAME') != None:
    file_handle = config.get_setting('NAME','FILENAME')


timestamp = time.strftime('%Y%m%d.%H%M')
file_name = (file_handle + "-" + timestamp
         + '.' + str(random.randint(100,999)))

# make backup directory if it does not already exist
if not os.path.exists(dest_dir):
	print "Creating \'", dest_dir,"\' as a destination for backups."
	os.makedirs(dest_dir)
	assert os.path.exists(dest_dir), "We tried to make a directory, but couldn't find it afterwards."
else:
	print "Found destination directory:", dest_dir

# begin printing exception-related messages
print ""

# set ignore_hidden
ignore_hidden = False
ignore_hidden_str = config.get_setting('EXCEPT','IGNORE_HIDDEN')
if ignore_hidden_str == "True" or ignore_hidden_str == "true":
    print "Ignoring hidden files and folders..."
    ignore_hidden = True

# print files and directories that will be ignored
print "Files that will be ignored:"
for exc in file_exceptions:
    print " "*4, exc
print "Directories that will be ignored:"
for exc in dir_exceptions:
    print " "*4, exc
print ""

# build list of files
total_list = file_lister(source_dir, ignore_hidden=True, file_exceptions=file_exceptions, dir_exceptions=dir_exceptions)

# 
print("Building file list and packing tarball...")

# create a tarfile object that is opened for appending,
# then recursively append each target to it
tar = tarfile.open(name=dest_dir+file_name+'.tar',mode='w')
for i in total_list:
	tar.add(name=i,recursive=True)
tar.close()
handle = dest_dir +  file_name + ".tar"

# check filesize for consent from user
proc = pash.ShellProc()
proc.run("du -sh " + handle + " | column -t|cut -d ' ' -f 1")
size = proc.get_val('stdout').rstrip('\n')
print("The total size of the files in the built tarball is: "),
termcolor.cprint(size, 'cyan')
print("The compressed backup will likely be smaller than this.\n")

# if 'auto' was passed to the script, do not ask for user confirmation
if len(sys.argv) > 1:
    if sys.argv[1] == 'auto':
        result = True
else:
    yn = menu_generator.YN_Menu(default="no")
    result = yn.run()
if result == False:
    print("Operation cancelled, deleting tarball.")
    os.remove(handle)
    sys.exit(1)

print("\nApplying lzma compression... (this may take several minutes)")

command = 'lrzip ' + handle
proc.run(command)
data = proc.get_val('stdout').rstrip('\n').split('\n')

print("Compression complete.")

# waits for the backup file to exist, then removes the tar
print ("Ensuring the backup file exists..."),
while os.path.exists(handle+".lrz") == False:
	pass
print("found it!\n")

print data[0]

command = "du -sh " + data[0].split(':')[1].lstrip(' ') + "| column -t | cut -d ' ' -f 1"
proc.run(command)
sys.stdout.write("Compressed backup size: ") 
termcolor.cprint(proc.get_val('stdout'), 'cyan')


for index, i in enumerate(data[1].split(' ')):
	if i == 'Compression' and data[1].split(' ')[index+1] == 'Ratio:':
		comp_ratio = data[1].split(' ')[index+2].rstrip('.\n')

sys.stdout.write("Compression ratio: ") 
termcolor.cprint(comp_ratio, 'cyan')


print("\nDeleting the uncompressed tarball.")
os.remove(handle)

print("Backup complete. Have a nice day.")


# begin sample configuration file
# remove the first layer of hashes to use

#[DIR]
## if empty, SRC_DIR will default to the "home" directory of the
## current user
#SRC_DIR=
#DEST_DIR=/backup/my-backup/
#
#
#[EXCEPT]
## exceptions should be comma-separated
## example: 
##   EXCEPTIONS=/this/dir,/noman/dir,
##
#DIR_EXCEPT=
#FILE_EXCEPT=
#
## IGNORE_HIDDEN will cause the script to ignore any file or directory
## that begins with a period
#IGNORE_HIDDEN=True
#
#
#[NAME]
## the output filename for the backup will begin with the following string
## example:
##   FILENAME=MyBackup
##
##   results in a file: MyBackup-20150106.1845.tar.lrz
#FILENAME=MyBackup
