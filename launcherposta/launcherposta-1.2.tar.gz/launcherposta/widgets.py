# -*- coding: utf8 -*-

# Copyright 2012-2015 Facundo Batista
#
# This program is free software: you can redistribute it and/or modify it
# under the terms of the GNU General Public License version 3, as published
# by the Free Software Foundation.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranties of
# MERCHANTABILITY, SATISFACTORY QUALITY, or FITNESS FOR A PARTICULAR
# PURPOSE.  See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along
# with this program.  If not, see <http://www.gnu.org/licenses/>.
#
# For further info, check  https://launchpad.net/launcherposta

"""GUI widgets."""

import Queue
import logging
import os
import threading

# stupid gtk3; pylint: disable=E0611
from gi.repository import Gtk, GdkPixbuf, GObject
# stupid gtk3; pylint: enable=E0611

BASEDIR = os.path.dirname(__file__)

DESCRIPTION = u"""\
A launcher. A real launcher.
One that lets you launch programs.

https://launchpad.net/launcherposta
"""

# get the pixbufs from the icons, to put in the different windows
ICONS = []
for size in (14, 32, 64, 192):
    iconfile = os.path.join(BASEDIR, 'logos', 'logo-%d.png' % (size,))
    ICONS.append(GdkPixbuf.Pixbuf.new_from_file(iconfile))

# the place where the applications desktop files are
APPS_DIR = "/usr/share/applications/"


def get_about_dialog(version):
    """Return the About dialog."""
    dlg = Gtk.AboutDialog()
    dlg.set_icon_list(ICONS)

    # texts
    dlg.set_program_name(u"LauncherPosta")
    dlg.set_comments(DESCRIPTION)
    dlg.set_copyright(u"© 2012 Facundo Batista")
    dlg.set_version(u"v." + str(version))

    # logo
    path_logo = os.path.join(BASEDIR, 'logos', 'logo-64.png')
    pixbuf = GdkPixbuf.Pixbuf.new_from_file(path_logo)
    dlg.set_logo(pixbuf)

    return dlg


def show_error_dialog(msg):
    """Show an error dialog."""
    dlg = Gtk.MessageDialog(None, Gtk.DialogFlags.MODAL, Gtk.MessageType.ERROR,
                            Gtk.ButtonsType.OK, msg)
    dlg.set_title("Error")
    dlg.set_icon_list(ICONS)
    dlg.run()
    dlg.hide()


class _AppsInfoRetriever(threading.Thread):
    """Thread that will collect the information of the apps."""

    done_flag = "DONE"

    def __init__(self, queue):
        self.queue = queue
        super(_AppsInfoRetriever, self).__init__()

    def run(self):
        """Main loop."""
        theme = Gtk.IconTheme.get_default()
        bilinear = GdkPixbuf.InterpType.BILINEAR
        for desktop_file in os.listdir(APPS_DIR):
            desktop_file = os.path.join(APPS_DIR, desktop_file)
            if not os.path.isfile(desktop_file):
                continue
            with open(desktop_file, 'rb') as fh:
                icon = None
                cmd = desc = ""
                for line in fh:
                    if line.startswith("Name="):
                        desc = line.split("=")[1].strip()
                    if line.startswith("Exec="):
                        cmd = line.split("=")[1].strip()
                        if cmd:
                            cmd = cmd.split()[0]
                    if line.startswith("Icon="):
                        icon = line.split("=")[1].strip()
            if not cmd and not desc:
                continue

            if icon:
                if icon[0] == '/':
                    # absolute path
                    try:
                        pixbuf = GdkPixbuf.Pixbuf.new_from_file(icon)
                    except:
                        pixbuf = None
                    else:
                        pixbuf = pixbuf.scale_simple(32, 32, bilinear)
                else:
                    # icon name
                    try:
                        pixbuf = theme.load_icon(icon, 32, 0)
                    except:
                        pixbuf = None
            else:
                pixbuf = None
            self.queue.put((pixbuf, desc, cmd))

        self.queue.put(self.done_flag)


class _ApplicationFinderDialog(Gtk.Dialog):
    """Dialog to select an application from the installed ones."""

    def __init__(self):
        # no, it's a new style class; pylint: disable=E1002
        buttons = (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
                   Gtk.STOCK_APPLY, Gtk.ResponseType.APPLY)
        super(_ApplicationFinderDialog, self).__init__(
            "Select an application", None, Gtk.DialogFlags.MODAL, buttons)

        # the list store/view
        self.list_store = Gtk.ListStore(GdkPixbuf.Pixbuf, str, str)
        self.list_view = Gtk.TreeView(self.list_store)

        renderer = Gtk.CellRendererPixbuf()
        tvcolumn = Gtk.TreeViewColumn("Icon", renderer, pixbuf=0)
        tvcolumn.set_resizable(True)
        self.list_view.append_column(tvcolumn)

        renderer = Gtk.CellRendererText()
        tvcolumn = Gtk.TreeViewColumn("Description", renderer, text=1)
        tvcolumn.set_resizable(True)
        self.list_view.append_column(tvcolumn)

        renderer = Gtk.CellRendererText()
        tvcolumn = Gtk.TreeViewColumn("Command", renderer, text=2)
        tvcolumn.set_resizable(True)
        self.list_view.append_column(tvcolumn)

        scrolledwindow = Gtk.ScrolledWindow()
        scrolledwindow.set_hexpand(True)
        scrolledwindow.set_vexpand(True)
        scrolledwindow.add(self.list_view)
        self.get_content_area().add(scrolledwindow)

        # set up out-thread retrieval
        self.apps_queue = Queue.Queue()
        _AppsInfoRetriever(self.apps_queue).start()
        GObject.idle_add(self.update_list().next)

        self.resize(500, 500)
        self.show_all()

    def update_list(self):
        """Update list view with the info sent from the apps finder."""
        while True:
            data = self.apps_queue.get()
            if data is _AppsInfoRetriever.done_flag:
                break

            # have data! update and yield True to keep being called
            self.list_store.append(data)
            yield True

        # we're done, yield False to say goodbye
        yield False

    def get_info(self):
        """Return the selected info by the user."""
        path = self.list_view.get_cursor()[0]
        row = self.list_store[path]
        pixbuf, desc, cmd = row
        return pixbuf, desc, cmd


class _AddCommandDialog(Gtk.Dialog):
    """Dialog to get all the info for a new command."""

    def __init__(self, pre_load=None):
        # no, it's a new style class; pylint: disable=E1002
        super(_AddCommandDialog, self).__init__("Choose a program", None,
                                                Gtk.DialogFlags.MODAL, ())
        self.set_icon_list(ICONS)
        self.logger = logging.getLogger("AddCommandWindow")
        self.logger.info("Starting: %s", pre_load)
        pre_icon_pixbuf, pre_desc, pre_cmd = pre_load or (None, None, None)
        self.table = table = Gtk.Table(3, 3)
        nicer = (0, 0, 10, 10)

        table.attach(Gtk.Label("Description:"), 0, 1, 0, 1, *nicer)
        self.info_desc = Gtk.Entry()
        self.info_desc.set_width_chars(30)
        if pre_desc is not None:
            self.info_desc.set_text(pre_desc)
        table.attach(self.info_desc, 1, 2, 0, 1, *nicer)

        table.attach(Gtk.Label("Command:"), 0, 1, 1, 2, *nicer)
        self.info_cmd = Gtk.Entry()
        self.info_cmd.set_width_chars(30)
        if pre_cmd is not None:
            self.info_cmd.set_text(pre_cmd)
        table.attach(self.info_cmd, 1, 2, 1, 2, *nicer)

        self.info_icon_button = Gtk.Button("click to set image")
        self.info_icon_pixbuf = pre_icon_pixbuf
        if pre_icon_pixbuf is not None:
            img = Gtk.Image.new_from_pixbuf(self.info_icon_pixbuf)
            self.info_icon_button.set_label("")
            self.info_icon_button.set_image(img)
            img.show()
        self.info_icon_button.connect("clicked", self._change_icon)
        table.attach(self.info_icon_button, 2, 3, 0, 2, *nicer)

        find_button = Gtk.Button.new_from_stock(Gtk.STOCK_FIND)
        find_button.set_label("Select an installed application")
        find_button.connect("clicked", self._find_apps)
        table.attach(find_button, 0, 3, 2, 3,
                     Gtk.AttachOptions.FILL, Gtk.AttachOptions.FILL, 10, 10)

        choose_file_button = Gtk.Button.new_from_stock(Gtk.STOCK_FIND)
        choose_file_button.set_label("Select a file")
        choose_file_button.connect("clicked", self._choose_file)
        table.attach(choose_file_button, 0, 4, 3, 4,
                     Gtk.AttachOptions.FILL, Gtk.AttachOptions.FILL, 10, 10)

        self.get_content_area().add(table)
        self.add_button(Gtk.STOCK_CANCEL, 0)
        if pre_load is None:
            button_action = Gtk.STOCK_ADD
        else:
            button_action = Gtk.STOCK_SAVE
        self.button_to_add = self.add_button(button_action, 1)

        # connect these signals here now that we have the button to add
        self.info_desc.connect("changed", self._review_activebuttons)
        self.info_cmd.connect("changed", self._review_activebuttons)
        self._review_activebuttons()

        self.show_all()

    def _review_activebuttons(self, *a):
        """Enable/disable some buttons according to rules."""
        # only allow adding if cmd and desc
        cmd_text = self.info_cmd.get_buffer().get_text()
        desc_text = self.info_desc.get_buffer().get_text()
        self.button_to_add.set_sensitive(cmd_text and desc_text)

    def get_info(self):
        """Return the user input info from the dialog."""
        cmd_text = self.info_cmd.get_buffer().get_text()
        desc_text = self.info_desc.get_buffer().get_text()
        self.logger.info("Returning info: icon=%s desc=%r cmd=%r",
                         self.info_icon_pixbuf, desc_text, cmd_text)
        return self.info_icon_pixbuf, desc_text, cmd_text

    def _change_icon(self, _):
        """Change the icon."""
        dlg = Gtk.FileChooserDialog(
            "Choose icon", self, Gtk.FileChooserAction.OPEN,
            (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL, Gtk.STOCK_OPEN, Gtk.ResponseType.ACCEPT))
        dlg.set_icon_list(ICONS)
        resp = dlg.run()
        dlg.hide()
        if resp == Gtk.ResponseType.ACCEPT:
            fname = dlg.get_filename()
            self.logger.info("Changing icon, filename: %r", fname)
            try:
                self.info_icon_pixbuf = GdkPixbuf.Pixbuf.new_from_file(fname)
            except Exception as err:
                self.logger.error("Couldn't load the pixbuf: %r", err)
                show_error_dialog(str(err))
                return

            self.logger.info("Changing icon, pixbuf ok: %s",
                             self.info_icon_pixbuf)
            img = Gtk.Image.new_from_pixbuf(self.info_icon_pixbuf)
            self.info_icon_button.set_label("")
            self.info_icon_button.set_image(img)
            img.show()

    def _choose_file(self, _):
        """Search for a file."""

        dlg = Gtk.FileChooserDialog(
            "Choose an excecutable file", self, Gtk.FileChooserAction.OPEN,
            (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL, Gtk.STOCK_OPEN, Gtk.ResponseType.ACCEPT))

        resp = dlg.run()
        dlg.hide()
        if resp == Gtk.ResponseType.ACCEPT:
            # actualizar self.info_cmd
            fname = dlg.get_filename()
            self.logger.info("Selected filename: %r", fname)
            self.info_cmd.set_text(fname)

    def _find_apps(self, _):
        """Find applications installed in the system."""
        dlg = _ApplicationFinderDialog()
        dlg.set_icon_list(ICONS)
        resp = dlg.run()
        dlg.hide()
        if resp == Gtk.ResponseType.APPLY:
            icon_pixbuf, desc, cmd = dlg.get_info()
            self.logger.info("Application selected: %s (%r)", desc, cmd)

            self.info_desc.set_text(desc)
            self.info_cmd.set_text(cmd)
            self.info_icon_pixbuf = icon_pixbuf
            if icon_pixbuf is not None:
                img = Gtk.Image.new_from_pixbuf(self.info_icon_pixbuf)
                self.info_icon_button.set_label("")
                self.info_icon_button.set_image(img)
                img.show()
            self._review_activebuttons()


class ConfigWindow(Gtk.Window):
    """The main configuration window."""

    def __init__(self, pre_load, apply_info_callback):
        # no, it's a new style class; pylint: disable=E1002
        super(ConfigWindow, self).__init__()
        self.pre_load = pre_load
        self.logger = logging.getLogger("ConfigWindow")
        self.logger.info("Starting: %s", pre_load)
        self.set_size_request(470, 300)
        self.apply_info_callback = apply_info_callback

        # title and icons
        self.set_title(u"Edit the menu")
        self.set_icon_list(ICONS)

        # the list of current stuff
        self.list_store = Gtk.ListStore(GdkPixbuf.Pixbuf, str, str)
        self.list_view = Gtk.TreeView(self.list_store)
        self.list_view.connect("cursor-changed", self._review_activebuttons)
        bilinear = GdkPixbuf.InterpType.BILINEAR
        for pre_pixbuf, pre_desc, pre_cmd in pre_load:
            if pre_pixbuf is not None:
                pre_pixbuf = pre_pixbuf.scale_simple(32, 32, bilinear)
            self.list_store.append((pre_pixbuf, pre_desc, pre_cmd))

        renderer = Gtk.CellRendererPixbuf()
        tvcolumn = Gtk.TreeViewColumn("Icon", renderer, pixbuf=0)
        tvcolumn.set_resizable(True)
        self.list_view.append_column(tvcolumn)

        renderer = Gtk.CellRendererText()
        tvcolumn = Gtk.TreeViewColumn("Description", renderer, text=1)
        tvcolumn.set_resizable(True)
        self.list_view.append_column(tvcolumn)

        renderer = Gtk.CellRendererText()
        tvcolumn = Gtk.TreeViewColumn("Command", renderer, text=2)
        tvcolumn.set_resizable(True)
        self.list_view.append_column(tvcolumn)

        # controls
        vbox2 = Gtk.VBox()
        cntrl_button_add = Gtk.Button.new_from_stock(Gtk.STOCK_ADD)
        cntrl_button_add.connect('clicked', self._item_add)
        cntrl_button_edit = Gtk.Button.new_from_stock(Gtk.STOCK_EDIT)
        cntrl_button_edit.connect('clicked', self._item_edit)
        cntrl_button_del = Gtk.Button.new_from_stock(Gtk.STOCK_DELETE)
        cntrl_button_del.connect('clicked', self._item_delete)
        cntrl_button_up = Gtk.Button.new_from_stock(Gtk.STOCK_GO_UP)
        cntrl_button_up.connect('clicked', self._item_move_up)
        cntrl_button_down = Gtk.Button.new_from_stock(Gtk.STOCK_GO_DOWN)
        cntrl_button_down.connect('clicked', self._item_move_down)
        vbox2.pack_start(cntrl_button_add, expand=False, fill=True, padding=2)
        vbox2.pack_start(cntrl_button_del, expand=False, fill=True, padding=2)
        vbox2.pack_start(cntrl_button_edit, expand=False, fill=True, padding=2)
        vbox2.pack_start(cntrl_button_up, expand=False, fill=True, padding=2)
        vbox2.pack_start(cntrl_button_down, expand=False, fill=True, padding=2)
        self.btns_change = [cntrl_button_edit, cntrl_button_del]
        self.btns_reorder = [cntrl_button_up, cntrl_button_down]

        # main hbox
        hbox1 = Gtk.HBox()
        hbox1.add(self.list_view)
        hbox1.pack_end(vbox2, expand=False, fill=True, padding=2)

        # close button
        close_button = Gtk.Button.new_from_stock(Gtk.STOCK_CLOSE)
        close_button.connect('clicked', lambda w: self.destroy())
        vbox2.pack_end(close_button, expand=False, fill=True, padding=2)

        self.add(hbox1)
        self._review_activebuttons()
        self.show_all()

    def _review_activebuttons(self, *a):
        """Enable/disable some buttons according to rules."""
        tree_selection = self.list_view.get_selection()
        if tree_selection is None:
            selection = False
        else:
            selection = tree_selection.get_selected()[1] is not None

        # change is possible if we have at least one item
        # and something selected
        allow_change = len(self.list_store) >= 1 and selection
        for button in self.btns_change:
            button.set_sensitive(allow_change)

        # for reorder we need at least two, and have something selected
        allow_reorder = len(self.list_store) >= 2 and selection
        for button in self.btns_reorder:
            button.set_sensitive(allow_reorder)

    def _item_move_up(self, _):
        """Move a line up."""
        self.logger.info("Moving item up")
        tree_selection = self.list_view.get_selection()
        tree_iter = tree_selection.get_selected()[1]
        swap_iter = self.list_store.iter_previous(tree_iter)
        if swap_iter is not None:
            self.list_store.move_before(tree_iter, swap_iter)
            self._apply_info()

    def _item_move_down(self, _):
        """Move a line down."""
        self.logger.info("Moving item down")
        tree_selection = self.list_view.get_selection()
        tree_iter = tree_selection.get_selected()[1]
        swap_iter = self.list_store.iter_next(tree_iter)
        if swap_iter is not None:
            self.list_store.move_after(tree_iter, swap_iter)
            self._apply_info()

    def _item_delete(self, _):
        """Delete a line."""
        self.logger.info("Deleting item")
        tree_selection = self.list_view.get_selection()
        treeiter = tree_selection.get_selected()[1]
        self.list_store.remove(treeiter)
        self._apply_info()
        self._review_activebuttons()

    def _item_add(self, _):
        """Add a line."""
        dlg = _AddCommandDialog()
        add_info = dlg.run()
        dlg.hide()
        if add_info:
            self.logger.info("Adding new item")
            icon, desc, cmd = dlg.get_info()
            if icon is not None:
                icon = icon.scale_simple(32, 32, GdkPixbuf.InterpType.BILINEAR)
            self.list_store.append([icon, desc, cmd])
            self._apply_info()
            self._review_activebuttons()

    def _item_edit(self, _):
        """Edit current line."""
        tree_selection = self.list_view.get_selection()
        treeiter = tree_selection.get_selected()[1]
        data = list(self.list_store[treeiter])
        dlg = _AddCommandDialog(data)
        save_info = dlg.run()
        dlg.hide()
        if save_info:
            new_info = dlg.get_info()
            self.logger.info("Edited an item, new stuff: %s", new_info)
            icon, desc, cmd = new_info
            self.list_store[treeiter] = [icon, desc, cmd]
            self._apply_info()

    def _apply_info(self):
        """Apply the info to the menu."""
        data = [list(row) for row in self.list_store]
        self.logger.info("Applying data: %s", data)
        self.apply_info_callback(data)


if __name__ == "__main__":
    # try it!
    GObject.threads_init()

#    dialog = get_about_dialog()
#    dialog.run()
#    dialog.hide()

#    window = ConfigWindow([], lambda _: None)
#    Gtk.main()

    dialog = _AddCommandDialog()
    dialog.run()
    dialog.hide()
