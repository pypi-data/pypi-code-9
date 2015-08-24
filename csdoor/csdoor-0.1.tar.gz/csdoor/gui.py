#!/usr/bin/python
import Tkinter
import os
from tkFileDialog import askopenfilename
from file_parser import FileParser
import ttk


def main():
    app = csDoor(None)
    app.title('csdoor')
    app.mainloop()


class csDoor(Tkinter.Tk):

    def __init__(self, parent):
        Tkinter.Tk.__init__(self, parent)
        self.parent = parent
        self.initialize()

    def initialize(self):
        self.grid()

        self.labelVariable = Tkinter.StringVar()
        label = Tkinter.Label(self, textvariable=self.labelVariable,
                              anchor="w")
        label.grid(column=0, row=0, columnspan=1,  rowspan=2, sticky='EW', pady=10)
        self.labelVariable.set(u"Select room number: ")

        self.entryVariable = Tkinter.StringVar()
        self.room_number = Tkinter.Entry(self, textvariable=self.entryVariable)
        self.room_number.grid(column=1, row=0, sticky='EW', pady=10)
        #self.room_number.bind("<Return>", self.OnPressEnter)


        self.sep = ttk.Separator(self, orient="horizontal")
        self.sep.grid(row=4, column=0, columnspan=2, sticky="ew", pady=15)

        self.labelVariable = Tkinter.StringVar()
        label = Tkinter.Label(self, textvariable=self.labelVariable,
                              anchor="w")
        label.grid(column=0, row=5, columnspan=1,  rowspan=2, sticky='EW')
        self.labelVariable.set(u"Upload name file:")

        button = Tkinter.Button(self, text=u"browse",
                                command=self.InputFilePath)
        button.grid(column=1, columnspan=1, rowspan=2, pady=5,sticky='EW', row=5)

        self.labelVariable = Tkinter.StringVar()
        label = Tkinter.Label(self, textvariable=self.labelVariable,
                              anchor="w")
        label.grid(column=0, row=10, columnspan=1,  rowspan=2, sticky='EW')
        self.labelVariable.set(u"Input file:")

        self.input_path = Tkinter.StringVar()
        label = Tkinter.Label(self, textvariable=self.input_path,
                              anchor="w")
        label.grid(column=1, row=10, columnspan=1,  rowspan=2, sticky='EW')


        #label = Tkinter.Label(self, textvariable=self.labelVariable,
                              #anchor="w", fg="white", bg="blue")

        self.sep = ttk.Separator(self, orient="horizontal")
        self.sep.grid(row=15, column=0, columnspan=2, sticky="ew", pady=15)

        self.labelVariable = Tkinter.StringVar()
        label = Tkinter.Label(self, textvariable=self.labelVariable,
                              anchor="w")
        label.grid(column=0, row=20, columnspan=1,  rowspan=2, sticky='EW', pady=5)
        self.labelVariable.set(u"Specify output file path: ")

        self.output_file_entry = Tkinter.StringVar()
        self.output_file = Tkinter.Entry(self, textvariable=self.output_file_entry)
        self.output_file.grid(column=1,columnspan=3, row=20, sticky='EW')
        self.output_file_entry.set(os.path.abspath(""))

        button = Tkinter.Button(self, text=u"Run",
                                command=self.Run)
        button.grid(column=0, columnspan=2, rowspan=2, pady=5,sticky='EW', row=25)

        # output
        self.labelVariable = Tkinter.StringVar()
        label = Tkinter.Label(self, textvariable=self.labelVariable,
                              anchor="w")
        label.grid(column=0, row=30, columnspan=1,  rowspan=2, sticky='EW')
        self.labelVariable.set(u"Output:")

        self.output = Tkinter.Text(self,height=75, width=75)
        self.output.insert(Tkinter.INSERT, "")

        self.output.grid(column=0, row=35, columnspan=2,  rowspan=10, sticky='EW')

        self.grid_columnconfigure(0, weight=1)
        #self.resizable(True, False)
        self.update()
        self.geometry(self.geometry())
        self.room_number.focus_set()
        self.room_number.selection_range(0, Tkinter.END)

    def InputFilePath(self):
        filepath = askopenfilename()
        self.input_path.set(filepath)

    def Run(self):
        filepath = self.input_path.get()
        file_parser = FileParser(filepath)
        output_file = self.output_file_entry.get()
        file_parser.create_room_auth_file(self.room_number.get(), output_file)
        if file_parser.found_errors:
            print("Parsing errors in input file, see errors.log for further details")
            with open("errors.log") as f:
                    for line in f:
                        self.output.insert(Tkinter.INSERT, line)
                        self.output.insert(Tkinter.INSERT, "\n")
        else:
            self.output.insert(Tkinter.INSERT, "File created successfully. No errors were found")


    def OnPressEnter(self, event):
        self.labelVariable.set(self.entryVariable.get() + " You pressed enter!")
        self.entry.focus_set()
        self.entry.selection_range(0, Tkinter.END)


if __name__ == "__main__":
    main()
