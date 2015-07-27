#!/usr/bin/env python

from __future__ import unicode_literals
import youtube_dl
import time
import os
import argparse

__ver__ = "0.01"
__author__ = "James Milne"

def clear_screen():
    """A nice little cross-platform way of clearing the console"""
    os.system(['clear','cls'][os.name == 'nt'])

def check_file_system():
    """A simple function to ensure the folder ~/youtube_me exists, and the download.list file exists inside that folder"""
    if not os.path.isdir(os.path.expanduser("~/youtube_me")):
        os.mkdir(os.path.expanduser("~/youtube_me"))
    if not os.path.isdir(os.path.expanduser("~/youtube_me/videos")):
        os.mkdir(os.path.expanduser("~/youtube_me/videos"))
    if not os.path.isfile(os.path.expanduser("~/youtube_me/download.list")):
        with open(os.path.expanduser("~/youtube_me/download.list"),'w+') as filePointer:
            filePointer.write("\n")

def get_time():
    """A simple way of getting input for the times to download within"""
    parser = argparse.ArgumentParser()
    parser.add_argument("-s", "--start-time", help="The 24 hour notation of the hour that you want to start downloading. e.g 13")
    parser.add_argument("-e", "--end-time", help="The 24 hour notation of the hour that you want to end downloading. e.g. 23")
    cliArgs = parser.parse_args()
    if cliArgs.start_time:
        startTime = int(cliArgs.start_time)
    else:
        startTime = 0
    if cliArgs.end_time:
        endTime = int(cliArgs.end_time)
    else:
        endTime = 24
    return {"startTime":startTime,"endTime":endTime}

def get_files():
    """The magic that uses youtube-dl to download our list, or print the time until downloading will happen"""
    startTime = int(get_time()['startTime'])
    endTime = int(get_time()['endTime'])
    infinite_loop = True
    while infinite_loop:
        if int(time.strftime("%H")) > startTime and int(time.strftime("%H")) < endTime:
            check_file_system()
            video_folder = os.path.expanduser("~/youtube_me/videos")
            video_title = video_folder + "/" + '%(title)s' + ".mp4"
            ydl_opts = {'nooverwrites':True,'outtmpl':video_title,'sleep-interval':'10'}
            with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                with open(os.path.expanduser("~/youtube_me/download.list"),'r') as filePointer:
                    for line in filePointer:
                        if int(time.strftime("%H")) > startTime and int(time.strftime("%H")) < endTime:
                            check_file_system()
                            if line.strip() != '':
                                ydl.download([line.strip("\n").strip("\r")])
        else:
            clear_screen()
            hours_til = 24 - int(time.strftime("%H"))
            mins_til = 60 - int(time.strftime("%M"))
            time_til = [hours_til,mins_til]
            print("Time till next download... " + str(time_til[0]) + ":" + str(time_til[1]))
            time.sleep(120)

if __name__ == '__main__':
    check_file_system()
    get_files()
