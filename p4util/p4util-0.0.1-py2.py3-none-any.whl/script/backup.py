#!/usr/bin/env python
from __future__ import print_function
import subprocess
import sys
import re
import argparse
import shutil
import gzip
import os

if sys.version_info[0] >= 3:
    from configparser import ConfigParser
else:
    from ConfigParser import ConfigParser

try:
    import P4
except ImportError:
    P4EXEC="Not set"

import string, logging, logging.handlers
from datetime import datetime

CONFIG = "backup.cfg"

class BufferingSMTPHandler(logging.handlers.BufferingHandler):
    def __init__(self, mailhost, fromaddr, toaddrs, subject, capacity, logfile=None):
        logging.handlers.BufferingHandler.__init__(self, capacity)
        self.mailhost = mailhost
        self.mailport = None
        self.fromaddr = fromaddr
        self.toaddrs = toaddrs
        self.subject = subject
        self.setFormatter(logging.Formatter("%(asctime)s %(levelname)-5s %(message)s"))
        self.logfile = None
        if logfile:
            self.logfile = open(logfile, "w")
 
    def flush(self):
        if len(self.buffer) > 0:
            try:
                import smtplib
                port = self.mailport
                if not port:
                    port = smtplib.SMTP_PORT
                smtp = smtplib.SMTP(self.mailhost, port)
                msg = "From: %s\r\nTo: %s\r\nSubject: %s\r\n\r\n" % (self.fromaddr, string.join(self.toaddrs, ","), self.subject)
                for record in self.buffer:
                    s = self.format(record)
                    if self.logfile:
                        print( s, file=self.logfile )
                    msg = msg + s + "\r\n"
                smtp.sendmail(self.fromaddr, self.toaddrs, msg)
                smtp.quit()
            except:
                self.handleError(None)  # no particular record
            self.buffer = []

class Backup:
    def __init__(self, configFile, loggingLevel):
        self.read_config_file(configFile)
        
        self.logger = logging.getLogger("")
        self.logger.setLevel(logging.DEBUG)
        
        subject = self.subject + " " + datetime.now().strftime("%Y/%m/%d %H:%M:%S")
        handler = BufferingSMTPHandler(self.mailHost, self.fromUser, self.toUsers, self.subject, self.capacity, self.logFile)
        self.logger.addHandler(handler)
 
    def read_config_file(self, configFile):
        self.parser = ConfigParser()
        try:
            with open(configFile) as f:
                self.parser.readfp(f)
        except:
            print( "Could not read {}".format( configFile ), file=sys.stderr )
            sys.exit(2)
        
        # check the sections, all sections have to be present
        
        sections = [ "p4", "bin", "mail", "log" ]
        for section in sections:
            if not self.parser.has_section(section):
                print( "Required section {} not present in config file".format(section), file=sys.stderr)
                sys.exit(3)
        
        self.p4root = self.read_config("p4", "P4ROOT")
        self.p4port = self.read_config("p4", "P4PORT")
        self.p4user = self.read_config("p4", "P4USER")
        self.p4passwd = self.read_config("p4", "P4PASSWD", "")
        self.p4log = self.read_config("p4", "P4LOG")
        self.p4prefix = self.read_config("p4", "P4PREFIX", "")
        
        self.p4dExec = self.read_config("bin", "P4D")
        self.p4Exec = self.read_config("bin", "P4", "")
        
        self.mailHost = self.read_config("mail", "MAILHOST")
        self.fromUser = self.read_config("mail", "FROM")
        
        to = self.read_config("mail", "TO")
        self.toUsers  = [ x.strip() for x in to.split(",")]
        self.subject = self.read_config("mail", "SUBJECT")
        self.capacity = int( self.read_config("mail", "CAPACITY", "10") )

        self.logFile = self.read_config("log", "BACKUP_LOG", "")
        self.logLevel = self.read_config("log", "LEVEL", "INFO")
        
    def read_config(self, section, option, default=None):
        if self.parser.has_option(section, option):
            return self.parser.get(section, option)
        elif default == None:
            print( 'Required option {} not found in section {}'.format(option, section), file=sys.stderr )
            sys.exit(1)
        else:
            return default


    def verify(self):        
        self.logger.info("Start verify ...")
        
        p4 = P4.P4()
        p4.port = self.p4port
        p4.user = self.p4user
        
        # should capture in try/catch failure to connect (server down?)
        # log, then continue with backup without verify
        
        try:
            p4.connect()
            
            if self.p4passwd: # only login if password provided, otherwise assume we have a ticket
                p4.password = self.p4passwd
                p4.run_login()
            
            p4.run_verify("-q", "//...", tagged=False, exception_level=0)
            if p4.errors:
                verifyErrors = "Verify reported errors:\n"
                verifyErrors += "\n".join(p4.errors)
                
                self.logger.error(verifyErrors)
        except P4.P4Exception as e:
            self.logger.error("Verify failed : " + str(e))
    
        self.logger.info("End verify ...")

    def checkpoint(self):
        self.logger.info("Start checkpoint ...")

        cmd = [ self.p4dExec, "-r", self.p4root, "-jc", "-Z" ]
        if self.p4prefix:
            cmd.append(self.p4prefix)
        
        p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out = p.stdout.read().decode()
        err = p.stderr.read().decode()

        result = True
                
        if err:
            self.logger.error("Backup failed with:\n" + err)
            result= False
        else:
            result = out.split("\n")
            
            pattern = re.compile("Rotating journal to (.+)\.(\d+)...")
            g = pattern.match(result[2])
            self.journalNumber = g.group(2)

        self.logger.info("End checkpoint ...")
        return result
    
    def rotate_log(self):
        
        newLogFile = self.p4prefix + ".log." + self.journalNumber
        shutil.move(self.p4log, newLogFile)
    
        compressed = newLogFile + ".gz"
        with open(newLogFile, "rb") as f:
            content = f.read()
        with gzip.open(compressed, "wb") as f:
            f.write(content)
            
        os.remove(newLogFile)
        
        self.logger.info("Truncated {} to {}".format(self.p4log, compressed))
        
if __name__ == "__main__":
    parser = argparse.ArgumentParser(
            description="Backup",
            epilog="Copyright (C) 2013 Sven Erik Knop, Perforce Software Ltd"
    )
    
    parser.add_argument("-c","--config", default=CONFIG, help="Config file to be used [default backup.cfg]")
    parser.add_argument('-v', '--verbose', 
                        nargs='?', 
                        const="DEBUG", 
                        default="INFO",
                        choices=('DEBUG', 'WARNING', 'INFO', 'ERROR', 'FATAL') ,
                        help="Various levels of debug output")
    options = parser.parse_args()
    
    backup = Backup(options.config, options.verbose)
    
    backup.verify()
    if backup.checkpoint():
        backup.rotate_log()
    