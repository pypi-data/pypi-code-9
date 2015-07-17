#!/usr/bin/env python
# -*- coding: utf-8 -*-

from tornado.web import RequestHandler, Application
from tornado.ioloop import IOLoop
from tornado.httpserver import HTTPServer

import logging, sys, time, os, zipfile, subprocess
import signal
import ssl

from marcopolo.bindings import polo
from marcobootstrap.slave import conf

programmed_updates = {}
programmed_reboots = {}

io_loop = None
settings = None
application = None
httpServer = None
import requests
import requests.packages.urllib3
requests.packages.urllib3.disable_warnings()

class UpdateHandler(RequestHandler):
    """
    A handler for update requests
    """
    def post(self):
        """
        Processes the POSTed form and schedules the update operation
        """
        bootcode = self.get_argument('bootcode', None)
        logging.debug(bootcode)
        #if bootcode is not None:
        #    bootcode = bootcode[0]

        image = self.get_argument('image', '')
        logging.debug(image)
        reboot_time = self.get_argument('time', None)

        #The reboot is not done if the time is not provided and 
        # it is performed instantaneously if it is equal to zero.
        if reboot_time is None:
            reboot = -1

        elif float(reboot_time) == 0.0:
            reboot = 0
        else:
            reboot = float(reboot_time)

        if reboot > 0:
            handle = io_loop.call_at(float(reboot_time), self.update, self.request.remote_ip, bootcode=bootcode, image=image)
            programmed_updates[float(reboot_time)] = handle

            self.set_status(101)
            self.finish("")
        else:
            self.set_status(101)
            self.finish("")
            self.update(self.request.remote_ip, bootcode=bootcode, image=image)

    def update(self, ip, bootcode=None, image=''):
        """
        Executes the update operation
        """
        def unzip_bootcode(source, dest_dir):
            """
            Unzips the bootcode into the desired location
            """
            #http://stackoverflow.com/a/640033/2628463
            zip_file = zipfile.ZipFile(source)
            zip_file.extractall(path=dest_dir)

        def process_bootcode(bootcode, image):
            """
            Processes the given bootcode
            """
            path = None
            if bootcode is None:
                path = conf.BOOTCODE_FALLBACK
            else:
                logging.info("Downloading bootcode %s for operation" % bootcode)
                r = requests.get("https://"+ip+":"+str(conf.BACKEND_FILES_PORT)+"/bootcode/download/"+bootcode, 
                                 stream=True, 
                                 verify=False,
                                 cert=(conf.APPCERT, conf.APPKEY))
                filename = bootcode
                with open(os.path.join(conf.TMP_DIR, filename), 'wb') as output_file:
                    for chunk in r.iter_content(chunk_size=1024): 
                        if chunk:
                            output_file.write(chunk)
                            output_file.flush()
                path = os.path.join(conf.TMP_DIR, filename)

            logging.debug(path)
            unzip_bootcode(path, conf.BOOTDIR)
            if image != '':
                with open(os.path.join(conf.BOOTDIR, "installer-config.txt"), 'w') as f_desc:
                    f_desc.write("export OS_IMG=%s" % image.replace(".tar.gz", ""))
        
        process_bootcode(bootcode, image)
        command = "shutdown -r +2 %s" % conf.REBOOT_MSG
        subprocess.Popen(command, shell=True)
        logging.info("An update is scheduled")

class CancelHandler(RequestHandler):
    """
    Accepts cancellation requests
    """
    def post(self):
        """
        Determines the id of the scheduled operation
        and removes it from the IOLoop
        """
        event_type = self.get_argument('type', None)

        if not event_type:
            self.set_status(400)
            self.finish("")
            return
        

        if event_type == "reboot":
            dictionary = programmed_reboots
        elif event_type == "update":
            dictionary = programmed_updates
        else:
            self.set_status(400)
            self.finish("")
            return

        reboot_time = self.get_argument('time', None)

        if reboot_time is not None:
            handle = dictionary.get(float(reboot_time))
            if handle is not None:
                io_loop.remove_timeout(handle)
                del dictionary[float(reboot_time)]
                logging.info("An event of type \"%s\" scheduled for %f has been removed!" % (event_type, float(reboot_time)))
                self.set_status(200)
                self.finish()
                return
        
        logging.warning("Event not found %f" % float(reboot_time))
        self.set_status(400)
        self.finish()
        

class RebootHandler(RequestHandler):
    """
    Schedules reboot operations
    """
    def post(self):
        """
        Processes reboot operations according to the submitted parameters
        """
        reboot_time = self.get_argument('time', None)
        if reboot_time is None:
            reboot = -1

        elif float(reboot_time) == 0.0:
            reboot = 0.0

        else:
            reboot = time.gmtime(float(reboot_time))

        if float(reboot_time) > 0.0:
            handle = io_loop.call_at(float(reboot_time), self.reboot)
            programmed_reboots[float(reboot_time)] = handle
            
            self.set_status(101)
            self.finish("")
        else:
            self.set_status(101)
            self.finish("")
            self.reboot()

    def reboot(self):
        """
        Reboots the system
        """
        command = "shutdown -r +2 %s" % conf.REBOOT_MSG
        subprocess.Popen(command, shell=True)

def shutdown():
    logging.info("Stopping gracefully")
    try:
        polo.Polo().unpublish_service(conf.SERVICE_NAME, delete_file=True)
    except Exception as e:
        logging.warning(e)
    io_loop.stop()

def sigint_handler(signal, frame):
    io_loop.add_callback(shutdown)

signal.signal(signal.SIGINT, sigint_handler)

def main(argv=None):
    """
    Starts the server, the logging facility and the IOLoop
    """
    global io_loop, settings, application, httpServer
    io_loop = IOLoop.instance()
    settings = {"debug":conf.DEBUG}

    application = Application([
        (r'/update/?', UpdateHandler),
        (r'/cancel/?', CancelHandler),
        (r'/reboot/?', RebootHandler),
    ], **settings)

    httpServer = HTTPServer(application, ssl_options={
        "certfile": conf.RECEIVERCERT,
        "keyfile": conf.RECEIVERKEY,
        "cert_reqs": ssl.CERT_REQUIRED,
        "ca_certs": conf.APPCERT}
    )
    httpServer.listen(conf.SLAVE_PORT)

    if not os.path.exists('/var/log/marcopolo'):
        os.makedirs('/var/log/marcopolo')

    logging.basicConfig(filename=conf.LOG_FILENAME, 
                        level=conf.LOG_LEVEL.upper())

    logging.info('Starting marco-bootstrap-backend-slave on port %s.' % conf.SLAVE_PORT)

    logging.info("Publishing marco service")

    
    while True:
        try:
            service_name =polo.Polo().publish_service(conf.SERVICE_NAME, root=True)
            logging.debug(service_name)
            break
        except polo.PoloInternalException as e:
            logging.warning(e)
            time.sleep(1)
        except polo.PoloException as i:
            logging.warning(i)
            break
        except Exception as e:
            logging.warning(e)
            time.sleep(1)

    logging.info("Listening on port %d" % conf.SLAVE_PORT)
    
    io_loop.start()

if __name__ == "__main__":
    main(sys.argv[1:])
