import time
import subprocess as sp
import sys
import signal

bla = sys.path
sys.path.append('/usr/lib/freecad/lib')
import FreeCAD as FreeCAD


def load():
    def signal_handler(signal, frame):
        raise (KeyboardInterrupt)

    import Part as Part

    signal.signal(signal.SIGINT, signal_handler)


load()

if __name__ == "__main__":
    try:
        i = 0
        while i < 20:
            print "a"
            i += 1
            time.sleep(1)
    except KeyboardInterrupt:
        print "bla"
        raise
