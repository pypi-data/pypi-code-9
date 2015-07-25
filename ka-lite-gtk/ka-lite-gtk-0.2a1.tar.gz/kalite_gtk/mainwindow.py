from __future__ import print_function
from __future__ import unicode_literals

from gi.repository import Gtk, Gdk, GLib, Pango
from pkg_resources import resource_filename  # @UnresolvedImport
import logging

from . import cli


logger = logging.getLogger(__name__)


def run_async(func):
    """
    http://code.activestate.com/recipes/576684-simple-threading-decorator/

        run_async(func)
            function decorator, intended to make "func" run in a separate
            thread (asynchronously).
            Returns the created Thread object

            E.g.:
            @run_async
            def task1():
                do_something

            @run_async
            def task2():
                do_something_too

    """
    from threading import Thread
    from functools import wraps

    @wraps(func)
    def async_func(*args, **kwargs):
        func_hl = Thread(target=func, args=args, kwargs=kwargs)
        func_hl.start()
        # Never return anything, idle_add will think it should re-run the
        # function because it's a non-False value.
        return None

    return async_func


class Handler:

    def __init__(self, mainwindow):
        self.mainwindow = mainwindow

    def on_delete_window(self, *args):
        Gtk.main_quit(*args)

    @run_async
    def on_start_button_clicked(self, button):
        self.log_message("Starting KA Lite...\n")
        GLib.idle_add(self.mainwindow.start_button.set_sensitive, False)
        for stdout, stderr, returncode in cli.start():
            if stdout:
                self.log_message(stdout)
        if returncode == 0:
            self.log_message("KA Lite started!\n")
        elif stderr:
            self.log_message(stderr)
        GLib.idle_add(self.mainwindow.start_button.set_sensitive, True)
        GLib.idle_add(self.mainwindow.update_status)

    @run_async
    def on_stop_button_clicked(self, button):
        GLib.idle_add(button.set_sensitive, False)
        self.log_message("Stopping KA Lite...\n")
        for stdout, stderr, returncode in cli.stop():
            if stdout:
                self.log_message(stdout)
        if returncode:
            self.log_message("Failed to stop\n")
        if stderr:
            self.log_message(stderr)
        GLib.idle_add(button.set_sensitive, True)
        GLib.idle_add(self.mainwindow.update_status)

    @run_async
    def on_diagnose_button_clicked(self, button):
        GLib.idle_add(button.set_sensitive, False)
        start_iter = self.mainwindow.diagnostics.get_start_iter()
        end_iter = self.mainwindow.diagnostics.get_end_iter()
        GLib.idle_add(lambda: self.mainwindow.diagnostics.delete(start_iter, end_iter))
        stdout, stderr, returncode = cli.diagnose()
        if stdout:
            GLib.idle_add(self.mainwindow.diagnostics_message, stdout)
        if stderr:
            GLib.idle_add(self.mainwindow.diagnostics_message, stderr)
        if returncode:
            GLib.idle_add(self.mainwindow.set_status, "Failed to diagnose!")
        GLib.idle_add(button.set_sensitive, True)

    @run_async
    def on_startup_service_button_clicked(self, button):
        GLib.idle_add(button.set_sensitive, False)
        if cli.is_installed():
            self.log_message("Removing startup service\n")
            stdout, stderr, returncode = cli.remove()
            if stdout:
                GLib.idle_add(self.log_message, stdout)
            if stderr:
                GLib.idle_add(self.log_message, stderr)
            if returncode:
                GLib.idle_add(self.log_message, "Failed to remove startup service\n")
        else:
            self.log_message("Installing startup service\n")
            stdout, stderr, returncode = cli.install()
            if stdout:
                GLib.idle_add(self.log_message, stdout)
            if stderr:
                GLib.idle_add(self.log_message, stderr)
            if returncode:
                GLib.idle_add(self.log_message, "Failed to install startup service\n")
        GLib.idle_add(self.mainwindow.set_from_settings)
        GLib.idle_add(button.set_sensitive, True)

    def on_main_notebook_change_current_page(self, *args, **kwargs):
        print(args, kwargs)

    def settings_changed(self, widget):
        """
        We should make individual handlers for widgets, but this is easier...
        """
        cli.save_settings()

    def log_message(self, msg):
        """Logs a message using idle callaback"""
        GLib.idle_add(self.mainwindow.log_message, msg)


class MainWindow:

    def __init__(self):

        self.builder = Gtk.Builder()
        glade_file = resource_filename(__name__, "glade/mainwindow.glade")
        self.builder.add_from_file(glade_file)

        # Save glade builder XML tree objects to object properties all in
        # one place so we don't get confused. Don't call get_object other places
        # PLEASE.
        self.window = self.builder.get_object('mainwindow')
        self.log_textview = self.builder.get_object('log_textview')
        self.diagnose_textview = self.builder.get_object('diagnose_textview')
        self.diagnostics = self.builder.get_object('diagnostics')
        self.status_entry = self.builder.get_object('status_label')
        self.default_user_radio_button = self.builder.get_object('radiobutton_user_default')
        self.kalite_command_entry = self.builder.get_object('kalite_command_entry')
        self.port_spinbutton = self.builder.get_object('port_spinbutton')
        self.content_root_filechooserbutton = self.builder.get_object('content_root_filechooserbutton')
        self.username_entry = self.builder.get_object('username_entry')
        self.username_radiobutton = self.builder.get_object('radiobutton_username')
        self.log = self.builder.get_object('log')
        self.start_button = self.builder.get_object('start_button')
        self.stop_button = self.builder.get_object('stop_button')
        self.diagnose_button = self.builder.get_object('diagnose_button')
        self.startup_service_button = self.builder.get_object('startup_service_button')

        # Auto-connect handlers defined in mainwindow.glade
        self.builder.connect_signals(Handler(self))

        # Style the log like a terminal
        self.log_textview.override_font(
            Pango.font_description_from_string('DejaVu Sans Mono 9')
        )
        self.log_textview.override_background_color(
            Gtk.StateFlags.NORMAL, Gdk.RGBA(0, 0, 0, 1))
        self.log_textview.override_color(
            Gtk.StateFlags.NORMAL, Gdk.RGBA(1, 1, 1, 1))
        self.log_textview.override_background_color(
            Gtk.StateFlags.SELECTED, Gdk.RGBA(0.7, 1, 0.5, 1))

        # Style the diagnose view like a terminal
        self.diagnose_textview.override_font(
            Pango.font_description_from_string('DejaVu Sans Mono 9')
        )
        self.diagnose_textview.override_background_color(
            Gtk.StateFlags.NORMAL, Gdk.RGBA(0, 0, 0, 1))
        self.diagnose_textview.override_color(
            Gtk.StateFlags.NORMAL, Gdk.RGBA(1, 1, 1, 1))
        self.diagnose_textview.override_background_color(
            Gtk.StateFlags.SELECTED, Gdk.RGBA(0.7, 1, 0.5, 1))

        self.set_from_settings()

        GLib.idle_add(self.update_status)
        GLib.timeout_add(60 * 1000, lambda: self.update_status or True)

        self.window.show_all()

    def diagnostics_message(self, msg):
        self.diagnostics.insert_at_cursor(msg)

    def log_message(self, msg):
        self.log.insert_at_cursor(msg)

    def set_from_settings(self):
        label = self.default_user_radio_button.get_label()
        label = label.replace('{default}', cli.DEFAULT_USER)
        self.default_user_radio_button.set_label(label)
        self.kalite_command_entry.set_text(cli.settings['command'])
        self.port_spinbutton.set_value(int(cli.settings['port']))

        self.content_root_filechooserbutton.set_filename(cli.settings['content_root'])

        if cli.DEFAULT_USER != cli.settings['user']:
            self.username_entry.set_text(cli.settings['user'])
            self.username_radiobutton.set_active(True)

        self.startup_service_button.set_sensitive(cli.has_init_d())
        if cli.has_init_d():
            if cli.is_installed():
                self.startup_service_button.set_label("Remove startup service")
            else:
                self.startup_service_button.set_label("Install startup service")

    @run_async
    def update_status(self):
        GLib.idle_add(self.set_status, "Updating status...")
        GLib.idle_add(self.set_status, "Server status: " + (cli.status() or "Error fetching status").split("\n")[0])

    def set_status(self, status):
        self.status_entry.set_label(status)


if __name__ == "__main__":
    win = MainWindow()
    Gtk.main()
