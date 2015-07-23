# -*- coding: utf-8 -*-

"""
2mp3.core
~~~~~~~~~~
The main module that converts your files to awesome mp3's.
"""

import envoy
from sys import argv, exit


cwd = None
if len(argv) > 1:
    cwd = argv[1]

# check whether ffmpeg is installed
ffmpeg = envoy.run('ffmpeg')

if 'No such file or directory' in ffmpeg.std_err:
    # ffmpeg isn't installed, install it.
    out = envoy.run("echo It seems like you dont have ffmpeg installed. \
                     Dont worry, 2mp3 will install it in a giffy").std_out
    print out

    envoy.run('sudo apt-add-repository -y ppa:jon-severinsson/ffmpeg') 
    envoy.run('sudo apt-get -y update')
    envoy.run('sudo apt-get -y install ffmpeg')

    out = "\n ffmpeg has been succesfully installed. continuing with conversion...\n"
    print out

list_all_in_dir = envoy.run('ls', cwd=cwd)
std_out = list_all_in_dir.std_out

if 'No such file or directory' in list_all_in_dir.std_err:
    print "the directory you provided does not exist."
    print "please provide a valid directory and rerun the command"
    exit()

split_em = std_out.split('\n')
split_em = filter(None, split_em) # remove empty items from list

print "BEGINNING CONVERSION, this may take a while.\n"
for song in split_em:
    the_cmd = 'ffmpeg -i "{0}" -f mp3 "{1}".mp3'.format(song, song)
    print "CONVERTING: {0} : INTO AN MP3 FILE...".format(song)
    convert = envoy.run(the_cmd, cwd=cwd)

    if argv[2] and argv[2] == '-r':
        envoy.run('rm -f "{0}"'.format(song), cwd=cwd) # remove original file



#envoy.run(command, data=None, timeout=None, kill_timeout=None, env=None, cwd=None)