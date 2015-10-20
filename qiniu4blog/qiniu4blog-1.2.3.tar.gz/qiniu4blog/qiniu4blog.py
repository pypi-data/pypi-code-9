#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os, time, sys ,ConfigParser,platform,urllib
import qiniu
from mimetypes import MimeTypes
import sys
import pyperclip
from os.path import expanduser
import signal
import time
import sys


homedir = expanduser("~")                           #get home dir path
config = ConfigParser.RawConfigParser()             #read config
config.read(homedir+'/qiniu.cfg')
mime = MimeTypes()

def exit_gracefully(signum, frame):
    # restore the original signal handler as otherwise evil things will happen
    # in raw_input when CTRL+C is pressed, and our signal handler is not re-entrant
    signal.signal(signal.SIGINT, original_sigint)

    try:
        if raw_input("\nReally quit? (y/n)> ").lower().startswith('y'):
            sys.exit(1)

    except KeyboardInterrupt:
        print("Ok ok, quitting")
        sys.exit(1)

    # restore the exit gracefully handler here
    signal.signal(signal.SIGINT, exit_gracefully)


original_sigint = signal.getsignal(signal.SIGINT)
signal.signal(signal.SIGINT, exit_gracefully)


try:
    bucket = config.get('config', 'bucket')         #set  bucket
    accessKey = config.get('config', 'accessKey')   #set  accessKey
    secretKey = config.get('config', 'secretKey')   #set  secretKey
    path_to_watch = config.get('config', 'path_to_watch')   #set image root dir
    enable = config.get('custom_url','enable')        #set custom_url
    if enable == 'false':
        print 'custom_url not set'
    else:
        addr = config.get('custom_url','addr')
except ConfigParser.NoSectionError, err:
    print 'Error Config File:', err

#set character coding
def setCodeingByOS():
    if 'cygwin' in platform.system().lower():
        CODE = 'GBK'
    elif os.name == 'nt' or platform.system() == 'Windows':
        CODE = 'GBK'
    elif os.name == 'mac' or platform.system() == 'Darwin':
        CODE = 'utf-8'
    elif os.name == 'posix' or platform.system() == 'Linux':
        CODE = 'utf-8'
    return  CODE

#set clipboard
def set_clipboard(url_list):
	for url in url_list:
		pyperclip.copy(url)
	spam = pyperclip.paste()


#print response from qiniu server
def parseRet(retData, respInfo):
    if retData != None:
        print("Upload file success!")
        print("Hash: " + retData["hash"])
        print("Key: " + retData["key"])
        for k, v in retData.items():
            if k[:2] == "x:":
                print(k + ":" + v)
        for k, v in retData.items():
            if k[:2] == "x:" or k == "hash" or k == "key":
                continue
            else:
                print(k + ":" + str(v))
    else:
        print("Upload file failed!")
        print("Error: " + respInfo.text_body)

#upload file style1
def upload_without_key(bucket, filePath, uploadname):
    auth = qiniu.Auth(accessKey, secretKey)
    upToken = auth.upload_token(bucket, key=None)
    key = uploadname
    retData, respInfo = qiniu.put_file(upToken, key, filePath, mime_type=mime.guess_type(filePath)[0])
    parseRet(retData, respInfo)

#upload file style2
def upload_with_full_Path(filePath):
    if platform.system() == 'Windows':
        fileName = "/".join("".join(filePath.rsplit(path_to_watch))[1:].split("\\"))
    else:
        fileName = "".join(filePath.rsplit(path_to_watch))[1:]
    upload_without_key(bucket, filePath, fileName.decode(setCodeingByOS()))
    if enable == 'true':
        url = addr + urllib.quote(fileName.decode(setCodeingByOS()).encode('utf-8'))
    else:
        url = 'http://' + bucket + '.qiniudn.com/' + urllib.quote(fileName.decode(setCodeingByOS()).encode('utf-8'))
    return url

#upload file style3
def upload_with_full_Path_cmd(filePath):
    if platform.system() == 'Windows':
        filePath = "/".join((filePath.split("\\")))
        fileName = os.path.basename(filePath)
    else:
        fileName = os.path.basename(filePath)
    upload_without_key(bucket, filePath, fileName.decode(setCodeingByOS()))
    if enable == 'true':
        url = addr + urllib.quote(fileName.decode(setCodeingByOS()).encode('utf-8'))
    else:
        url = 'http://' + bucket + '.qiniudn.com/' + urllib.quote(fileName.decode(setCodeingByOS()).encode('utf-8'))
    return url

#get all file path on root image dir
def get_filepaths(directory):
    file_paths = []  # List which will store all of the full filepaths.
    for root, directories, files in os.walk(directory):
        for filename in files:
            # Join the two strings in order to form the full filepath.
            filepath = os.path.join(root, filename)
            file_paths.append(filepath)  # Add it to the list.
    return file_paths  # Self-explanatory.




def main():
    if len(sys.argv) > 1:
        url_list = []
        for i in sys.argv[1:]:
            url = upload_with_full_Path_cmd(i)
            url_list.append(url)
        with open('image_markdown.txt', 'a') as f:
            for url in url_list:
                image = '![' + url + ']' + '(' + url + ')' + '\n'
                print url,'\n'
                f.write(image)
        print "\nNOTE: save image url [markdown] in image_markdwon.txt"
        set_clipboard(url_list)
        return
    print "running ... ... \nPress Ctr+C to Stop"
    before =  get_filepaths(path_to_watch)
    while 1:
        time.sleep(1)
        after = get_filepaths(path_to_watch)
        added = [f for f in after if not f in before]
        removed = [f for f in before if not f in after]
        if added:
            print "Added Files: ", ", ".join(added)
            url_list = []
            for i in added:
                url = upload_with_full_Path(i)
                url_list.append(url)
            with open('image_markdown.txt', 'a') as f:
                for url in url_list:
                    image = '![' + url + ']' + '(' + url + ')' + '\n'
                    print url,'\n'
                    f.write(image)
            print "\nNOTE: save image url [markdown] in image_markdwon.txt"
            set_clipboard(url_list)
        if removed:
            print "Removed Files: ", ", ".join(removed)
            print  removed
        before = after



if __name__ == "__main__":
    main()


