"""
Yanker

Usage:
    yanker [--threads=<tnum>]
"""
__version__ = '1.0.1'

import Queue
import threading
import youtube_dl as ydl
import pyperclip as clip
import time
from docopt import docopt


class ErrLogger(object):
    def debug(self, msg):
        pass

    def warning(self, msg):
        pass

    def error(self, msg):
        print msg


class Worker(threading.Thread):
    def __init__(self, tasks):
        threading.Thread.__init__(self)
        self.tasks = tasks
        self.daemon = True
        self.start()

    def run(self):
        while True:
            vid = self.tasks.get()
            vid.download()
            self.tasks.task_done()


class Video:
    def progress(self, s):
        if s['status'] == 'finished':
            print 'Finished {}'.format(s['filename'])

    def __init__(self, url, opts={}):
        self.url = url
        self.ydl_opts = {
            'progress_hooks': [self.progress],
            'logger': ErrLogger()
        }
        self.ydl_opts.update(opts)

    def download(self):
        print 'Downloading: {}'.format(self.url)
        with ydl.YoutubeDL(self.ydl_opts) as y:
            try:
                y.download([self.url])
            except ydl.DownloadError:
                print 'Unsupported URL, skipping'


class Watcher:
    def __init__(self, urls=[], threads=2):
        self.queue = Queue.Queue(0)
        self.threads = threads
        self.stopped = False
        self.grabbed_urls = set([])
        for _ in range(threads): Worker(self.queue)

    def run(self):
        recent = ''
        while not self.stopped:
            current = clip.paste()
            if recent != current:
                recent = current
                if current.startswith(('http://', 'https://',)) and current not in self.grabbed_urls:
                    print 'Added: {}'.format(current)
                    self.grabbed_urls.add(current)
                    self.queue.put(Video(current))
                elif current in self.grabbed_urls:
                    print 'Already grabbed {}'.format(current)
            time.sleep(0.25)


def run():
    args = docopt(__doc__, version='Yanker {}'.format(__version__))
    threads = args['--threads']
    if not threads:
        threads = 2
    else:
        threads = int(threads)
    print 'Starting Yanker with {} threads...'.format(threads)
    watch = Watcher(threads=threads)
    try:
        watch.run()
    except KeyboardInterrupt:
        print 'Stopping...'
        watch.stopped = True
