
import sys
import signal
import time
import os
import timeit

from copy import copy
from multiprocessing import Pipe, Process
from threading import Thread
from abc import abstractmethod
from bdb import BdbQuit
from codeop import compile_command

import pykd
from pykd import *

from karmadbg.dbgcore.dbgdecl import *
from karmadbg.dbgcore.nativedbg import NativeDebugger
from karmadbg.dbgcore.pydebug import PythonDebugger
from karmadbg.dbgcore.macro import *
from karmadbg.dbgcore.util import *

class ConsoleDebugClient(AbstractDebugClient):

    def quit(self):
       pass

    def output(self,str):
        sys.stdout.write(str)

    def input(self):
        return sys.stdin.readline()

    def onTargetStateChanged(self,state):
        pass

    def onTargetChangeCurrentThread(self):
        pass

    def onTargetChangeCurrentFrame(self, frame):
        pass

    def onTargetChangeBreakpoints(self):
        pass

    def onPythonStart(self):
        return False

    def onPythonQuit(self):
        pass

    def onPythonStateChange(self,state):
        pass

    def onPythonBreakpointAdd(self, file, line):
        pass

    def onPythonBreakpointRemove(self, file, line):
        pass


class DebugServer(object):

    def startServer(self):

        signal.signal( signal.SIGINT, signal.SIG_IGN)

        self.clientOutput = self.getClientOutput()

        sys.stdin = self
        sys.stdout = self
        sys.stderr = self

        self.nativeDbg = NativeDebugger(self)
        self.pythonDbg = PythonDebugger(self)

        self.interruptServer = self.processServerInterrupt(self)
        self.commandServer = self.processServerCommand(self)

        print
        print "start debug server"
        self.startup()

        self.nativeCommandLoop()


    def pythonCommandLoop(self):
        self.commandServer.sendAnswer(None)
        self.commandLoop(self.pythonDbg)

    def nativeCommandLoop(self):
        self.commandLoop(self.nativeDbg)

    def commandLoop(self, commandHandler):

        commandHandler.outputPrompt()

        while not self.commandServer.stopped:

            methodName, args, kwargs = self.commandServer.getRequest()

            try:

                if methodName == 'quit':
                    self.quit()
                    self.commandServer.sendAnswer(None)
                    continue

                if methodName == 'debugCommand':
                    if self.debugCommand(commandHandler, *args, **kwargs):
                        return
                    self.commandServer.sendAnswer(None)
                    commandHandler.outputPrompt()
                    continue

                if methodName == 'callFunction':
                    try:
                        result = args[0](*args[1:],**kwargs)
                    except Exception, ex:
                        result = ex
                    self.commandServer.sendAnswer(result)
                    continue

                if methodName == 'startup':
                    self.startup()
                    self.commandServer.sendAnswer(None)
                    continue
 
                # Native DBG command ( windbg )
                if hasattr(self.nativeDbg, methodName):
                    res = getattr(self.nativeDbg, methodName)(*args, **kwargs)
                    self.commandServer.sendAnswer(res)
                    continue

                # Python DBG command 
                if hasattr(self.pythonDbg, methodName):
                    res = getattr(self.pythonDbg, methodName)(*args, **kwargs)
                    self.commandServer.sendAnswer(res)
                    continue

                self.commandServer.sendAnswer(None)

            except:

                sys.stderr.write(showtraceback( sys.exc_info(), 2 ))
                self.commandServer.sendAnswer(None)

    def debugCommand(self, commandHandler, commandStr):

        if not commandStr:
            return False

        if commandHandler is self.nativeDbg:

            if self.nativeDbg.debugCommand(commandStr):
                return

            if self.isMacroCmd(commandStr):
                self.macroCmd(commandStr)
                return

            self.pythonCommand(commandStr)

            return False

        elif commandHandler is self.pythonDbg:

            return self.pythonDbg.debugCommand(commandStr)

    def write(self,str):
        self.clientOutput.output(str)

    def readline(self):
        return self.clientOutput.input()

    def flush(self):
        pass

    def breakin(self):
        if self.pythonDbg.breakin():
            return
        self.nativeDbg.breakin()

    def quit(self):
        self.interruptServer.stop()
        self.commandServer.stop()

    def isMacroCmd(self,commandStr):
        return commandStr[0] == '%'

    def macroCmd(self,commandStr):

        try:
            vars = commandStr.split()

            if vars[0] == "%run":
                self.runCodeCommand(vars[1:], debug = False)
            elif vars[0] == "%rund":
                self.runCodeCommand(vars[1:], debug = True)
            elif vars[0] == "%exec":
                self.execCode(" ".join(vars[1:]), debug = False)
            elif vars[0] == "%execd":
                self.execCode(" ".join(vars[1:]), debug = True )
            elif vars[0] == "%time":
                t1 = time.clock()
                ret = self.nativeDbg.debugCommand(" ".join(vars[1:]))
                t2 = time.clock()
                print "time elapsed: %fs" % (t2-t1)
                self.commandServer.sendAnswer(ret)
            else:
                macroCommand(commandStr)

        except SystemExit:
            print "macro command raised SystemExit"

        except:
            print showtraceback(sys.exc_info())

    def runCodeCommand(self, vars, debug = False):

        if len(vars) == 0:
            return

        fileName = vars[0]
        args = vars[1:]

        argv = sys.argv
        syspath = sys.path

        dirname, _ = os.path.split(fileName)

        if not dirname:
            script, suffix = os.path.splitext(fileName)
            try:
                _,fileName,desc=imp.find_module(script)
            except ImportError:
                sys.stderr.write("module \'%s\' not found\n" % script)
                self.commandServer.sendAnswer(None)
                return
        else:
            sys.path.append(dirname)

        try:
            
            sys.argv = []
            sys.argv.append(fileName)
            sys.argv.extend(args)

            import __builtin__

            glob = {}
            glob['__builtins__'] = __builtin__
            glob["__name__"] = "__main__"
            glob["__file__"] = fileName
            glob["__doc__"] = None
            glob["__package__"] = None

            if debug:
                self.pythonDbg.execfile(fileName,glob,glob)
            else:
                execfile(fileName, glob, glob)

        except SystemExit:
            print "script raised SystemExit"

        except:
            sys.stderr.write(showtraceback( sys.exc_info(), 2 ))

        sys.argv = argv
        sys.path = syspath

        sys.stdin = self
        sys.stdout = self
        sys.stderr = self


    def execCode(self, codestr, debug = False):

        if not codestr:
            return

        try:

            codeObject = compile(codestr, "<input>", "single")

            if debug:
                self.pythonDbg.execcode(codeObject, globals(), globals())
            else:
                exec codeObject in globals()

        except SystemExit:
            print "expression raised SystemExit"

        except:
            print showtraceback( sys.exc_info(), 2 )


    def pythonCommand(self, commandStr):

        code = None
        try:
            while True:
                code = compile_command(commandStr, "<input>", "single")
                if code:
                    break
                commandStr += "\n" + raw_input('...')

        except SyntaxError:
            print showtraceback(sys.exc_info(), 3)
            return

        try:
            exec code in globals()

        except SystemExit:
            self.getClientEventHandler().quit()

        except:
            print showtraceback(sys.exc_info())

    def startup(self):
        #from karmadbg.startup.firstrun import firstrun
        from karmadbg.startup.startup import startup
        #firstrun()
        startup()

    #def getAutoComplete(self, startAutoComplete):
    #    return []

class LocalProxy(object):

    def __init__(self, pipe):
        self.pipe = pipe

    def __getattr__(self, methodname):

        class callToPipe(object):

            def __init__(self,pipe):
                self.pipe=pipe

            def __call__(self, *args, **kwargs):
                self.pipe.send( (methodname, args, kwargs) )
                result = self.pipe.recv()
                if isinstance(result, Exception):
                    raise result
                return result

        return callToPipe(self.pipe)


class LocalStub(object):

    def __init__(self, pipe, requestHandler):
        self.pipe = pipe
        self.requestHandler = requestHandler
        self.stopped = False

    def getRequest(self):
        return self.pipe.recv()

    def sendAnswer(self, answer):
        return self.pipe.send(answer)

    def stop(self):
        self.stopped = True

class LocalThreadApartmentStub(LocalStub):

    def __init__(self, pipe, requestHandler):
        super(LocalThreadApartmentStub,self).__init__(pipe,requestHandler)
        self.workThread = Thread(target=self.threadRoutine)
        self.workThread.start()

    def threadRoutine(self):

        while not self.stopped:
            if self.pipe.poll(1):
                methodName, args, kwargs = self.getRequest()
                try:
                    result = getattr(self.requestHandler, methodName)(*args, **kwargs)
                except Exception, ex:
                    result = ex
                self.sendAnswer(result)

    def stop(self):
        self.stopped = True
        self.workThread.join()


class LocalDebugServer(DebugServer,Process):

    def __init__(self):
        self.outputPipe, outputServerPipe = Pipe()
        self.commandPipe, commandServerPipe = Pipe()
        self.interruptPipe, interruptServerPipe = Pipe()
        self.eventPipe, eventServerPipe = Pipe()
        self.outputStub = None
        self.eventStub = None
        self.interruptStub = None
        self.commadStub = None
        self.stopped = False

        DebugServer.__init__(self)
        Process.__init__(self, target = self.processRoutine, args = (outputServerPipe, commandServerPipe, interruptServerPipe, eventServerPipe))

    def processRoutine(self, outputPipe, commandPipe, interruptPipe, eventPipe ):

        self.outputPipe = outputPipe
        self.commandPipe = commandPipe
        self.interruptPipe = interruptPipe
        self.eventPipe = eventPipe

        self.startServer()

    def getClientOutput(self):
        return LocalProxy(self.outputPipe)

    def getClientEventHandler(self):
        return LocalProxy(self.eventPipe) 

    def getServerControl(self):
        return LocalProxy(self.commandPipe)

    def getServerInterrupt(self):
        return LocalProxy(self.interruptPipe)

    def processClientOutput(self, requestHandler):
        if not self.outputStub:
            self.outputStub  = LocalThreadApartmentStub(self.outputPipe, requestHandler)
        return self.outputStub

    def processClientEvents(self, requestHandler):
        if not self.eventStub:
            self.eventStub = LocalThreadApartmentStub(self.eventPipe, requestHandler)
        return self.eventStub

    def processServerInterrupt(self, requestHandler):
        if not self.interruptStub:
            self.interruptStub = LocalThreadApartmentStub( self.interruptPipe, requestHandler)
        return self.interruptStub

    def processServerCommand(self, requestHandler):
        if not self.commadStub:
            self.commandStub = LocalStub(self.commandPipe, requestHandler)
        return self.commandStub
        


class DbgEngine(object):
    
    def __init__(self, dbgClient, dbgServer, dbgSettings):
        self.dbgServer = dbgServer
        self.dbgClient = dbgClient
        self.dbgSettings = dbgSettings

    def start(self):
        #start server
        self.dbgServer.start()

        #start client callback thread-apartment handlers
        self.outputStub = self.dbgServer.processClientOutput(self.dbgClient)
        self.eventsStub = self.dbgServer.processClientEvents(self.dbgClient)

    def stop(self):

        #stop debug server
        self.dbgServer.getServerInterrupt().breakin()
        self.dbgServer.getServerControl().quit()

        #stop client callback thread-apartment handlers
        self.outputStub.stop()
        self.eventsStub.stop()
        
    def getServer(self):
        return self.dbgServer

    def getClient(self):
        return self.dbgClient
