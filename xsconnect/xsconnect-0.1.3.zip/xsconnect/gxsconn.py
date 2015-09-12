# MIT license
# 
# Copyright (C) 2015 by XESS Corp.
# 
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
# 
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
'''
A GUI for generating pin location constraints for a peripheral board attached to a StickIt! motherboard.
'''

import sys
from os.path import join, basename, splitext
import Tkinter as tk
import tkFileDialog
import tkMessageBox
import ScrolledText
from xsconnect import *
from __init__ import __version__


class ScrollList(tk.Frame):
    '''Create a frame widget with a list and an attached scrollbar and title.'''

    def __init__(self, parent, title, list_entries):

        # Make the master frame.
        tk.Frame.__init__(self, parent)
        self.config()
        self.pack(fill='both', expand='yes')

        # Place title at top of master frame.
        self.title = tk.Label(self, text=title)
        self.title.pack(side=tk.TOP)

        # Make a subframe to hold the listbox and scrollbar.
        self.scroll_list = tk.Frame(self)
        self.scroll_list.config()
        # Place subframe below title.
        self.scroll_list.pack(fill='both', expand='yes')

        # Make the scrollbar and listbox inside the subframe.
        self.scrollbar = tk.Scrollbar(self.scroll_list)
        self.list = tk.Listbox(self.scroll_list)
        # Link listbox to scrollbar position. Disable exporting of the selection so multiple
        # listboxes can all show their selected items simultaneously.
        self.list.config(yscrollcommand=self.scrollbar.set,
                         selectmode=tk.SINGLE,
                         exportselection=0)
        # Link the scrollbar to the listbox.
        self.scrollbar.config(command=self.list.yview)
        # Attach scrollbar and listbox to the right and left sides of the subframe.
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.list.pack(side=tk.LEFT, fill=tk.BOTH, expand=1)
        # Place selectable entries into listbox.
        self.update_list(list_entries)

    def update_list(self, list_entries):
        '''Update the list entries in the listbox if the list entries have changed.'''
        current_list = set(self.list.get(0, tk.END))
        if current_list != set(list_entries):
            self.list.delete(0, tk.END)
            self.list.insert(0, *sorted(list_entries))
            self.list.activate(0)
            self.list.selection_set(0)


class Gxstie:
    '''Class for application.'''

    def save_as(self):
        name = tkFileDialog.asksaveasfile(mode='w', defaultextension=".ucf")
        name.write(str(self.assignments.get(0.0, tk.END)))
        name.close

    def show_help(self):
        pass

    def show_about(self):
        about_txt = splitext(basename(__file__))[0] + ' V' + str(__version__)
        tkMessageBox.showinfo('About', about_txt)

    def exit(self):
        sys.exit(0)

    def __init__(self, parent):

        # Create the main frame with an upper and lower pane.
        self.parent = parent
        self.main_frame = tk.PanedWindow(parent)
        self.main_frame.config(sashwidth=6,
                               showhandle=False,
                               relief=tk.GROOVE,
                               sashrelief=tk.FLAT,
                               orient=tk.VERTICAL)
        self.main_frame.pack(fill='both', expand='yes')

        # Create menu and submenus.
        self.menu = tk.Menu(self.parent)
        self.parent.config(menu=self.menu)
        # File submenu.
        self.file_menu = tk.Menu(self.menu, tearoff=0)
        self.file_menu.add_command(label='Save As...', command=self.save_as)
        self.file_menu.add_separator()
        self.file_menu.add_command(label='Exit', command=self.exit)
        self.menu.add_cascade(label='File', menu=self.file_menu)
        # Help submenu.
        self.help_menu = tk.Menu(self.menu, tearoff=0)
        self.help_menu.add_command(label='Help Contents',
                                   command=self.show_help)
        self.help_menu.add_separator()
        self.help_menu.add_command(
            label='About ' + splitext(basename(__file__))[0],
            command=self.show_about)
        self.menu.add_cascade(label='Help', menu=self.help_menu)

        # Create another four-paned window that goes at the top of the main frame.
        self.selector_frame = tk.PanedWindow(self.main_frame)
        self.selector_frame.config(sashwidth=6,
                                   showhandle=False,
                                   relief=tk.GROOVE,
                                   sashrelief=tk.FLAT,
                                   orient=tk.HORIZONTAL)
        self.selector_frame.pack(fill='both', expand='yes')

        # Create four scrolling lists to add to the four-paned window:
        # 1) Peripheral board scrolling list.
        self.periph_selector = ScrollList(self.selector_frame,
                                          'Peripheral Modules',
                                          get_board_list(PERIPHERALBRD_DIR))
        self.periph_list = self.periph_selector.list
        self.periph_list.bind('<<ListboxSelect>>', self.do_assignments)

        # 2) Motherboard scrolling list.
        self.mother_selector = ScrollList(self.selector_frame, 'Motherboards',
                                          get_board_list(MOTHERBRD_DIR))
        self.mother_list = self.mother_selector.list
        self.mother_list.bind('<<ListboxSelect>>', self.do_assignments)

        # 3) Motherboard port scrolling list.
        self.port_selector = ScrollList(self.selector_frame, 'Ports', [])
        self.port_list = self.port_selector.list
        self.port_list.bind('<<ListboxSelect>>', self.do_assignments)

        # 4) Daughterboard scrolling list.
        self.daughter_selector = ScrollList(self.selector_frame,
                                            'Daughter Boards',
                                            get_board_list(DAUGHTERBRD_DIR))
        self.daughter_list = self.daughter_selector.list
        self.daughter_list.bind('<<ListboxSelect>>', self.do_assignments)

        # Add the four scrolling lists to the four-paned window.
        self.selector_frame.add(self.periph_selector)
        self.selector_frame.add(self.mother_selector)
        self.selector_frame.add(self.port_selector)
        self.selector_frame.add(self.daughter_selector)

        # Create scrolling textbox for showing pin assignments in the lower pane of the main frame.
        self.assignments = ScrolledText.ScrolledText(self.main_frame)
        self.assignments.pack(fill='both', expand='yes')
        self.assignments.delete(1.0, tk.END)

        # Create a popup menu for copying & selecting assignments in the textbox.
        self.popupmenu = tk.Menu(root, tearoff=0)
        self.popupmenu.add_command(label="Copy", command=self.text_copy)
        self.popupmenu.add_separator()
        self.popupmenu.add_command(label="Select All",
                                   command=lambda: self.text_select_all(0))
        # Also assign shortcut keys for copy & select operations.
        self.assignments.bind('<Control-Key-a>', self.text_select_all)
        self.assignments.bind("<Button-3>", self.text_popup)

        # Add the four-paned window and the textbox to the main frame.
        self.main_frame.add(self.selector_frame)
        self.main_frame.add(self.assignments)

        # Initialize the assignments textbox.
        self.do_assignments(None)

    def text_copy(self):
        root.clipboard_clear()
        root.clipboard_append(self.assignments.selection_get())

    def text_select_all(self, *event):
        self.assignments.tag_add(tk.SEL, "1.0", tk.END)
        self.assignments.mark_set(tk.INSERT, "1.0")
        self.assignments.see(tk.INSERT)
        return 'break'

    def text_popup(self, event):
        self.popupmenu.post(event.x_root, event.y_root)

    def do_assignments(self, *event):
        try:
            peripheral_name = self.periph_list.get(
                self.periph_list.curselection()[0])
            mother_name = self.mother_list.get(
                self.mother_list.curselection()[0])
            compatible_ports = get_compatible_ports(MOTHERBRD_DIR, mother_name,
                                                    PERIPHERALBRD_DIR,
                                                    peripheral_name)
            compatible_ports = set([
                mbrd_prt for [mbrd_prt, pbrd_prt] in compatible_ports
            ])
            self.port_selector.update_list(compatible_ports)
            port_name = self.port_list.get(self.port_list.curselection()[0])
            daughter_name = self.daughter_list.get(
                self.daughter_list.curselection()[0])
            self.assignments.delete(1.0, tk.END)
            assignments = do_assignments(peripheral_name, mother_name,
                                         port_name, daughter_name)
            self.assignments.insert(tk.END, assignments_to_string(
                peripheral_name, mother_name, port_name, daughter_name,
                assignments))
        except IndexError:
            self.assignments.delete(1.0, tk.END)
            pass


root = tk.Tk()  # Make the root window global.

def gxsconn():
    root.title(splitext(basename(__file__))[0])
    icon_file = join(INSTALL_DIR, 'xess.gif')
    icon = tk.PhotoImage(file=icon_file)
    root.tk.call('wm', 'iconphoto', root._w, icon)
    gxstie = Gxstie(root)
    root.mainloop()

    
if __name__ == '__main__':
    gxsconn()
