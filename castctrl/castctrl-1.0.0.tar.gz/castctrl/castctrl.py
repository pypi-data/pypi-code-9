#!/usr/bin/env python
from __future__ import print_function

import pychromecast
import argparse
import subprocess
import os
import socket
import sys

__progname__ = "castctrl"

def turn_on_tv(cast):
    cast.start_app("CC1AD845") # com.google.cast.media, the default mp4 player
    cast.quit_app()

def play_video(url, cast, port=8000):
    if not "http://" in url or "https://" in url:
        # Finding local IP for url
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect((cast.host,8008))
        local_ip = s.getsockname()[0]
        s.close()
        process = subprocess.Popen(['nohup', 'python', '-m', 'SimpleHTTPServer', str(port)],
                                   stdout=open('/dev/null', 'w'),
                                   stderr=open('/tmp/cast.log', 'a'),
                                   preexec_fn=os.setpgrp )
        print("Web server started for current directory ({}) at http://{}:{}. You can stop this web server (after the video finishes) with 'kill {}'.".format(os.getcwd(), local_ip, port, process.pid), file=sys.stderr)
        url = "http://{}:8000/{}".format(local_ip, url)
    cast.play_media((url), "video/mp4")

def pause_video(cast):
    cast.media_controller.pause()

def stop_video(cast):
    cast.quit_app()

def main():
    casts = pychromecast.get_chromecasts_as_dict()
    parser = argparse.ArgumentParser(prog=__progname__)
    parser.add_argument("--url", help="URL of media to play. You should probably specify this if nothing else.")
#    parser.add_argument("-p", "--pause", help="Pause playback", action='store_true')
    parser.add_argument("--power", help="Turn on TV and switch to Chromecast", action="store_true")
    parser.add_argument("-s", "--stop", help="Stop playback", action='store_true')
    parser.add_argument("-d", "--device", help="Select device. List devices with -D")
    parser.add_argument("-D", "--devices", help="List devices", action='store_true')
    parser.add_argument("--port", help="Specify port for web server (if you pick a local file above)", type=int)
    args = parser.parse_args()
    if args.devices:
        print(", ".join(casts.keys()), file=sys.stderr)
        return
    if args.device:
        cast = casts[args.device]
    else:
        cast = casts[next(iter(casts))]
    if args.power:
        power_on_tv(cast)
        return
    if args.url:
        play_video(args.url, cast)
        return
#    elif args.pause:
#        pause_video(cast)
#        return
    elif args.stop:
        stop_video(cast)
        return

if __name__ == "__main__":
    main()
