#!/usr/bin/env python

from telnetlib import Telnet
from threading import Thread
import sys
from utils import port_path
import socket
import time
import os


def start_shell(port, host="127.0.0.1"):
    telnet = Telnet(host=host, port=port)

    def print_output():
        while True:
            try:
                out = telnet.read_eager()
                if out:
                    sys.stdout.write(out)
                    sys.stdout.flush()
            except EOFError:
                break

    Thread(target=print_output).start()
    try:
        while True:
            try:
                telnet.write(raw_input() + "\r\n")
            except (KeyboardInterrupt, EOFError):
                break
    finally:
        telnet.close()


def main():
    try:
        while True:
            path = port_path()
            try:
                with open(path) as portfile:
                    port = int(portfile.read())
                    print "\n\n==== Connecting on port %i... ====\n" % port
                    start_shell(port)
                    print "\n==== Disconnected. ===="
            except (IOError, socket.error):
                pass
            finally:
                try:
                    os.remove(path)
                except OSError:
                    pass
                time.sleep(0.3)
    except KeyboardInterrupt:
        pass


if __name__ == "__main__":
    main()
