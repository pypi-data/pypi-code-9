import SimpleHTTPServer
import SocketServer
import re
import cgi
from transat.server.job import Job
import threading
import Queue
import json
import os


class Server(object):

    """TransAT Server

    This class allow to run TransAT in a new Thread.
    TransAT commands can be send by http requests

    """

    def __init__(self):
        Handler = ServerHandler
        PORT = 0  # 8100
        I = ""
        self.httpd = SocketServer.TCPServer((I, PORT), Handler)
        self.httpd.current_job = None
        self.httpd.last_job = None
        self.httpd.jobs = Queue.Queue()
        I, PORT = self.httpd.server_address
        self.address = "http://localhost:" + str(PORT)
        self.filename = "sim.log"
        print "Serving at: http://%(interface)s:%(port)s" % dict(interface=I or "localhost", port=PORT)

    def run(self):
        """

        Launch the server

        """


        processor = threading.Thread(target=self.process_jobs)
        processor.daemon = True
        processor.start()
        self.httpd.serve_forever()

    def get_address(self):
        """ Return the URL of the server

        Args:
            url (str): url of the server

        """
        return self.address

    def process_jobs(self):
        while (-1):
            if not self.httpd.jobs.empty():
                    job = self.httpd.jobs.get()
                    self.httpd.last_job = job
                    self.httpd.current_job = job
                    job.run()
                    self.httpd.current_job = None


class ServerHandler(SimpleHTTPServer.SimpleHTTPRequestHandler):
    def log_message(self, format, *args):
        pass

    def has_jobs(self):
        if self.server.current_job is None and self.server.jobs.empty():
            return False
        else:
            return True

    def get_current_iteration(self):
        value = 0
        wd = self.server.last_job.wd
        fname = os.path.join(wd, 'sim.log')
        with open(fname) as f:
            content = f.readlines()
        flag = False
        for l in content:
            if "Iterating to Steady State" in l:
                flag = True
            m = re.match(r"\s+[0-9]+\s+[0-9]+", l)
            if m and flag:
                value = m.group(0).split()[0]
        return value

    def get_current_timestep(self):
        value = 0
        wd = self.server.last_job.wd
        fname = os.path.join(wd, 'sim.log')
        with open(fname) as f:
            content = f.readlines()
        for l in content:
            m = re.match(r"\s+Time step:\s+([0-9]+)\s.+", l)
            if m:
                value = m.group(0)
        return value


    def get_remaining_time(self):
        hours = 0
        minutes = 0
        wd = self.server.last_job.wd
        fname = os.path.join(wd, 'sim.log')
        with open(fname) as f:
            content = f.readlines()
            for l in content:
                m = re.match(r".+Simulation Time Remaining:\s+([0-9]+h)\s+([0-9]+m)\s.+", l)
                if m:
                    hours = m.groups()[0][:-1]
                    minutes = m.groups()[1][:-1]
        time = float(minutes)+float(hours)*60.0
        return time


    def do_GET(self):
        data = {}
        if self.path == '/jobs':
            data = {'value': self.has_jobs()}
        elif self.path == '/iteration':
            data = {'value': self.get_current_iteration()}
        elif self.path == '/timestep':
            data = {'value': self.get_current_timestep()}

        elif self.path == '/remainingTime':
            data = {'value': self.get_remaining_time()}

        self.send_response(200)
        self.send_header("Content-type", "application/json")
        self.wfile.write("\n")
        self.wfile.write(json.dumps(data))


    def do_POST(self):
        if self.path == '/stop':
            print "stop"
        else:
            form = cgi.FieldStorage(
                fp=self.rfile,
                headers=self.headers,
                environ={'REQUEST_METHOD': 'POST',
                         'CONTENT_TYPE': self.headers['Content-Type'],
                         })
            wd = form.getlist('wd')[0]
            fun = form.getlist('fun')[0]
            nprocs = form.getlist('nprocs')[0]
            job = Job(wd=wd, nprocs=nprocs, fun=fun)
            self.server.jobs.put(job)

        SimpleHTTPServer.SimpleHTTPRequestHandler.do_GET(self)





