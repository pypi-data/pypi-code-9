#!/usr/bin/env python3
#
# Copyright (C) 2012 Sven Erik Knop, Perforce Software Ltd
#
# Idea:
# Sync files from the default location (or, with -p, -u, -c, -H, -P options)
# Show progress using the Tkinter.tkk ProgressBar, P4.OutputHandler and P4.Progress
#

from __future__ import print_function

from argparse import ArgumentParser
import P4

try:
	import Tkinter as tk
	import ttk
	import Queue as queue
except ImportError:
	import tkinter as tk
	from tkinter import ttk
	import queue

import threading
import sys

class P4Command:
	def __init__(self):
		self.parser = ArgumentParser(
			description=self.description(),
			epilog="Copyright (C) 2012 Sven Erik Knop, Perforce Software Ltd"
		)
		self.parser.add_argument('-p', '--port', 		help="P4PORT")
		self.parser.add_argument('-c', '--client',		help="P4CLIENT")
		self.parser.add_argument('-u', '--user',		help="P4USER")
		self.parser.add_argument('-H', '--host',		help="P4HOST")
		self.parser.add_argument('-P', '--password',	help="P4PASSWD")
		self.parser.add_argument('-d', '--directory',	help="CWD")

		self.addArguments()

		self.myOptions = self.parser.parse_args()
		self.p4 = P4.P4()
		
		if self.myOptions.port:
			self.p4.port = self.myOptions.port
		if self.myOptions.client:
			self.p4.client = self.myOptions.client
		if self.myOptions.user:
			self.p4.user = self.myOptions.user
		if self.myOptions.host:
			self.p4.host = self.myOptions.host
		if self.myOptions.password:
			self.p4.password = self.myOptions.password
		if self.myOptions.directory:
			self.p4.cwd = self.myOptions.directory

	def description(self):
		return "P4Command"
	
	def addArguments(self):
		pass

class GuiPart(tk.Tk):
	def __init__(self, p4submit, queue):
		tk.Tk.__init__(self)
		
		self.columnconfigure(0, weight=1)
		self.rowconfigure(0, weight=1)
		
		self.title("P4 Submit")
		mainframe = ttk.Frame(self, padding="3 3 12 12 ")
		mainframe.grid(column=0, row=0, sticky="NWSE")
		mainframe.columnconfigure(0, weight=1) # resize progress bar horizontally
		mainframe.rowconfigure(0, weight=0)    # don't move the progress bar up or down
		mainframe.columnconfigure(1, weight=0) # and leave the label and button where they are 
		mainframe.rowconfigure(1, weight=1)    # resize the output listbox
		self.queue = queue
		self.p4sync = p4submit
		
		self.progress = ttk.Progressbar(mainframe, orient="horizontal", length=300, mode="determinate")
		self.progress.grid(column=0, row=0, sticky="EW")
		
		self.progress["value"] = 0
		self.progress["maximum"] = 100

		self.percent = tk.StringVar()
		self.percent.set("0.0 %")
		ttk.Label(mainframe, textvariable=self.percent).grid(column=1, row=0)
		
		frame = ttk.Frame(mainframe)
		frame.grid(column=0, row=1,sticky="NSEW")

		frame.columnconfigure(0, weight=1)
		frame.rowconfigure(0, weight=1)
		
		self.yscrollbar= ttk.Scrollbar(frame, orient=tk.VERTICAL)
		self.yscrollbar.grid(column=1, row=0, sticky="NS")
		
		self.xscrollbar = ttk.Scrollbar(frame, orient=tk.HORIZONTAL)
		self.xscrollbar.grid(column=0, row=1, sticky="EW")
		
		self.listbox = tk.Listbox(frame, height=10,width=40, 
								yscrollcommand=self.yscrollbar.set,
								xscrollcommand=self.xscrollbar.set)
		self.listbox.grid(column=0, row=0, sticky="NSEW" )
		
		self.yscrollbar["command"] = self.listbox.yview
		self.xscrollbar["command"] = self.listbox.xview
		

		self.button = ttk.Button(mainframe, text="Submit", command=p4submit.start)
		self.button.grid(column=1,row=1,sticky=tk.S)
		
		for child in mainframe.winfo_children(): child.grid_configure(padx=5, pady=5)

	def periodicCall(self):
		self.processIncoming()
			
		self.after(100, self.periodicCall)
	
	class StartRefresh:
		def __init__(self):
			pass
		def apply(self, gui):
			gui.button.configure(text="Cancel")
			gui.button.configure(command=gui.p4sync.cancel)
	
	class FinishedRefresh:
		def __init__(self):
			pass
		def apply(self, gui):
			gui.button.configure(text="Quit")
			gui.button.configure(command=gui.p4sync.quit)
	
	class DescriptionRefresh:
		def __init__(self, description, unit):
			self.description = description
			self.unit = unit
		def apply(self, gui):
			gui.title(self.description)
			gui.progress["value"] = 0
	
	class UpdateRefresh:
		def __init__(self, value):
			self.value = value
		def apply(self, gui):
			gui.progress["value"] = self.value
			gui.percent.set("%.1f %%" % self.value)
	
	class DoneRefresh:
		def __init__(self, filename, totalFileSize):
			self.filename = filename
			self.totalFileSize = totalFileSize
		def apply(self, gui):
			gui.listbox.insert(tk.END, "{name}\t{size:>8} KB".format(name=self.filename, size=self.totalFileSize))
			gui.listbox.yview(tk.END)

	
	def processIncoming(self):
		"""Read from queue, process results"""
		
		while self.queue.qsize():
			try:
				refresh = self.queue.get(0)
				refresh.apply(self)
			except queue.Empty:
				pass


class P4Submit(P4Command):
	def __init__(self):
		P4Command.__init__(self)
		
		if not self.myOptions.description and not self.myOptions.change:
			print( "Need to provide either change number '--change #' or description '--description text'")
			sys.exit(1)
		
		self.queue = queue.Queue()
		self.gui = GuiPart(self, self.queue)
		
	def addArguments(self):
		self.parser.add_argument('--change', dest='change', action='store', help="Change to be submitted")
		self.parser.add_argument('--description', dest='description', action='store', help="Description for default change")

	def description(self):
		return "P4Submit"
	
	class Callback(P4.Progress, P4.OutputHandler):
		def __init__(self, queue):
			self.queue = queue
			self.totalFileCount = 0
			self.totalFileSize = 0		
			self.response=P4.OutputHandler.HANDLED
				
		def outputMessage(self, message):
			print("Error: ", message)
			return P4.OutputHandler.CANCEL
		
		def init(self, type):
			self.type = type
	
		def setDescription(self, description, unit):
			refresh = GuiPart.DescriptionRefresh(description, unit)
			self.filename = description
			
			self.queue.put(refresh)			
			
		def setTotal(self, total):
			self.totalFileSize = total
	
		def update(self, position):
			self.position = position
			
			# print("Position: %s" % position)

			refresh = GuiPart.UpdateRefresh(100 * int(position) / self.totalFileSize)
			
			self.queue.put( refresh )
	
		def done(self, fail):
			self.fail = fail
			self.queue.put( GuiPart.DoneRefresh(self.filename, self.totalFileSize) )

	def start(self):
		self.thread = threading.Thread(target=self.runInThread)
		self.thread.start()
		
		self.queue.put(GuiPart.StartRefresh())
		
		self.gui.periodicCall()
	
	def cancel(self):
		self.callback.response=P4.OutputHandler.CANCEL
	
	
	def quit(self):
		import sys
		sys.exit(0)
	
	def runInThread(self):
		with self.p4.connect():
			args = []
			if self.myOptions.change: # is None if no options specified
				args.append('-c') 
				args.append(self.myOptions.change)
			elif self.myOptions.description:
				args.append('-d')
				args.append('self.myOptions.description')
			self.callback = P4Submit.Callback(self.queue)
			
			print( args )
				
			result = self.p4.run_submit(args, progress=self.callback, handler=self.callback, exception_level=0)
		self.queue.put(GuiPart.FinishedRefresh())
	
if __name__ == '__main__':
	p4submit = P4Submit()
	p4submit.gui.mainloop()

	