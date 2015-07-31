"""
Module defining the Core class, which is the central orchestrator
of poezio and contains the main loop, the list of tabs, sets the state
of everything; it also contains global commands, completions and event
handlers but those are defined in submodules in order to avoir cluttering
this file.
"""
import logging

log = logging.getLogger(__name__)

import asyncio
import os
import pipes
import sys
import time
from gettext import gettext as _

from slixmpp.xmlstream.handler import Callback

import connection
import events
import singleton
import tabs
import theming
import handlers

from bookmarks import BookmarkList
from config import config, firstrun
from daemon import Executor
from fifo import Fifo
from logger import logger
from plugin_manager import PluginManager
from roster import roster

from . structs import possible_show, DEPRECATED_ERRORS, \
        ERROR_AND_STATUS_CODES, Status


class Core(object):
    """
    “Main” class of poezion
    """

    def __init__(self):
        # All uncaught exception are given to this callback, instead
        # of being displayed on the screen and exiting the program.
        self.connection_time = time.time()
        status = config.get('status')
        status = possible_show.get(status, None)
        self.status = Status(show=status,
                message=config.get('status_message'))
        self.running = True
        self.xmpp = singleton.Singleton(connection.Connection)
        roster.set_node(self.xmpp.client_roster)
        self.bookmarks = BookmarkList()
        self.debug = False
        self.remote_fifo = None
        own_nick = config.get('default_nick')
        own_nick = own_nick or self.xmpp.boundjid.user
        own_nick = own_nick or os.environ.get('USER')
        own_nick = own_nick or 'poezio'
        self.own_nick = own_nick
        self.plugins_autoloaded = False
        self.plugin_manager = PluginManager(self)
        self.events = events.EventHandler()

        # Set to True whenever we consider that we have been disconnected
        # from the server because of a legitimate reason (bad credentials,
        # or explicit disconnect from the user for example), in that case we
        # should not try to auto-reconnect, even if auto_reconnect is true
        # in the user config.
        self.legitimate_disconnect = False

        # Add handlers
        self.initial_joins = []

        self.connected_events = {}

        self.pending_invites = {}
    def sigusr_handler(self, num, stack):
        """
        Handle SIGUSR1 (10)
        When caught, reload all the possible files.
        """
        log.debug("SIGUSR1 caught, reloading the files…")
        self.reload_config()

    def exit_from_signal(self, *args, **kwargs):
        """
        Quit when receiving SIGHUP or SIGTERM or SIGPIPE

        do not save the config because it is not a normal exit
        (and only roster UI things are not yet saved)
        """
        sig = args[0]
        signals = {
                1: 'SIGHUP',
                13: 'SIGPIPE',
                15: 'SIGTERM',
                }

        log.error("%s received. Exiting…", signals[sig])
        if config.get('enable_user_mood'):
            self.xmpp.plugin['xep_0107'].stop()
        if config.get('enable_user_activity'):
            self.xmpp.plugin['xep_0108'].stop()
        if config.get('enable_user_gaming'):
            self.xmpp.plugin['xep_0196'].stop()
        self.plugin_manager.disable_plugins()
        self.disconnect('%s received' % signals.get(sig))
        self.xmpp.add_event_handler("disconnected", self.exit, disposable=True)

    def autoload_plugins(self):
        """
        Load the plugins on startup.
        """
        plugins = config.get('plugins_autoload')
        if ':' in plugins:
            for plugin in plugins.split(':'):
                self.plugin_manager.load(plugin)
        else:
            for plugin in plugins.split():
                self.plugin_manager.load(plugin)
        self.plugins_autoloaded = True

    def start(self):
        if firstrun:
            self.information(_(
                'It seems that it is the first time you start poezio.\n'
                'The online help is here http://doc.poez.io/\n'
                'No room is joined by default, but you can join poezio’s'
                'chatroom (with /join poezio@muc.poez.io), where you can'
                ' ask for help or tell us how great it is.'),
                _('Help'))
        self.xmpp.plugin['xep_0012'].begin_idle(jid=self.xmpp.boundjid)

    def exit(self, event=None):
        log.debug("exit(%s)" % (event,))
        asyncio.get_event_loop().stop()

    def on_exception(self, typ, value, trace):
        """
        When an exception is raised, just reset curses and call
        the original exception handler (will nicely print the traceback)
        """
        try:
            self.reset_curses()
        except:
            pass
        sys.__excepthook__(typ, value, trace)

    def save_config(self):
        """
        Save config in the file just before exit
        """
        ok = roster.save_to_config_file()
        ok = ok and config.silent_set('info_win_height',
                                      self.information_win_size,
                                      'var')
        if not ok:
            self.information(_('Unable to save runtime preferences'
                               ' in the config file'),
                             _('Error'))

##################### Anything related to command execution ###################
    def exec_command(self, command):
        """
        Execute an external command on the local or a remote machine,
        depending on the conf. For example, to open a link in a browser, do
        exec_command(["firefox", "http://poezio.eu"]), and this will call
        the command on the correct computer.

        The command argument is a list of strings, not quoted or escaped in
        any way. The escaping is done here if needed.

        The remote execution is done
        by writing the command on a fifo.  That fifo has to be on the
        machine where poezio is running, and accessible (through sshfs for
        example) from the local machine (where poezio is not running). A
        very simple daemon (daemon.py) reads on that fifo, and executes any
        command that is read in it. Since we can only write strings to that
        fifo, each argument has to be pipes.quote()d. That way the
        shlex.split on the reading-side of the daemon will be safe.

        You cannot use a real command line with pipes, redirections etc, but
        this function supports a simple case redirection to file: if the
        before-last argument of the command is ">" or ">>", then the last
        argument is considered to be a filename where the command stdout
        will be written. For example you can do exec_command(["echo",
        "coucou les amis coucou coucou", ">", "output.txt"]) and this will
        work. If you try to do anything else, your |, [, <<, etc will be
        interpreted as normal command arguments, not shell special tokens.
        """
        if config.get('exec_remote'):
            # We just write the command in the fifo
            fifo_path = config.get('remote_fifo_path')
            if not self.remote_fifo:
                try:
                    self.remote_fifo = Fifo(os.path.join(fifo_path,
                                                         'poezio.fifo'),
                                            'w')
                except (OSError, IOError) as exc:
                    log.error('Could not open the fifo for writing (%s)',
                               os.path.join(fifo_path, './', 'poezio.fifo'),
                               exc_info=True)
                    self.information('Could not open the fifo '
                                     'file for writing: %s' % exc,
                                     'Error')
                    return

            args = (pipes.quote(arg.replace('\n', ' ')) for arg in command)
            command_str = ' '.join(args) + '\n'
            try:
                self.remote_fifo.write(command_str)
            except (IOError) as exc:
                log.error('Could not write in the fifo (%s): %s',
                            os.path.join(fifo_path, './', 'poezio.fifo'),
                            repr(command),
                            exc_info=True)
                self.information('Could not execute %s: %s' % (command, exc),
                                 'Error')
                self.remote_fifo = None
        else:
            executor = Executor(command)
            try:
                executor.start()
            except ValueError as exc:
                log.error('Could not execute command (%s)',
                          repr(command),
                          exc_info=True)
                self.information('%s' % exc, 'Error')

########################## TImed Events #######################################

    def remove_timed_event(self, event):
        """Remove an existing timed event"""
        event.handler.cancel()

    def add_timed_event(self, event):
        """Add a new timed event"""
        event.handler = asyncio.get_event_loop().call_later(event.delay,
                                                            event.callback,
                                                            *event.args)

####################### XMPP-related actions ##################################

    def get_status(self):
        """
        Get the last status that was previously set
        """
        return self.status

    def set_status(self, pres, msg):
        """
        Set our current status so we can remember
        it and use it back when needed (for example to display it
        or to use it when joining a new muc)
        """
        self.status = Status(show=pres, message=msg)
        if config.get('save_status'):
            ok = config.silent_set('status', pres if pres else '')
            msg = msg.replace('\n', '|') if msg else ''
            ok = ok and config.silent_set('status_message', msg)
            if not ok:
                self.information(_('Unable to save the status in '
                                   'the config file'), 'Error')

    def get_bookmark_nickname(self, room_name):
        """
        Returns the nickname associated with a bookmark
        or the default nickname
        """
        bm = self.bookmarks[room_name]
        if bm:
            return bm.nick
        return self.own_nick

    def disconnect(self, msg='', reconnect=False):
        """
        Disconnect from remote server and correctly set the states of all
        parts of the client
        """
        self.legitimate_disconnect = True
        msg = msg or ''
        # TODO: trigger a disconnect event
        self.xmpp.disconnect()
        if reconnect:
            # Add a one-time event to reconnect as soon as we are
            # effectively disconnected
            self.xmpp.add_event_handler('disconnected', lambda event: self.xmpp.connect(), disposable=True)

    def invite(self, jid, room, reason=None):
        """
        Checks if the sender supports XEP-0249, then send an invitation,
        or a mediated one if it does not.
        TODO: allow passwords
        """
        def callback(iq):
            if not iq:
                return
            if 'jabber:x:conference' in iq['disco_info'].get_features():
                self.xmpp.plugin['xep_0249'].send_invitation(
                        jid,
                        room,
                        reason=reason)
            else: # fallback
                self.xmpp.plugin['xep_0045'].invite(room, jid,
                        reason=reason or '')

        self.xmpp.plugin['xep_0030'].get_info(jid=jid, timeout=5,
                                              callback=callback)

    def get_error_message(self, stanza, deprecated=False):
        """
        Takes a stanza of the form <message type='error'><error/></message>
        and return a well formed string containing the error informations
        """
        sender = stanza.attrib['from']
        msg = stanza['error']['type']
        condition = stanza['error']['condition']
        code = stanza['error']['code']
        body = stanza['error']['text']
        if not body:
            if deprecated:
                if code in DEPRECATED_ERRORS:
                    body = DEPRECATED_ERRORS[code]
                else:
                    body = condition or _('Unknown error')
            else:
                if code in ERROR_AND_STATUS_CODES:
                    body = ERROR_AND_STATUS_CODES[code]
                else:
                    body = condition or _('Unknown error')
        if code:
            message = _('%(from)s: %(code)s - %(msg)s: %(body)s') % {
                    'from': sender, 'msg': msg, 'body': body, 'code': code}
        else:
            message = _('%(from)s: %(msg)s: %(body)s') % {
                    'from': sender, 'msg': msg, 'body': body}
        return message

####################### XMPP Event Handlers  ##################################
class XMPPHandlers(object):
    def __init__(self, xmpp):
        self.xmpp = xmpp
        self.xmpp.add_event_handler('connecting', self.on_connecting)
        self.xmpp.add_event_handler('connected', self.on_connected)
        self.xmpp.add_event_handler('connection_failed', self.on_failed_connection)
        self.xmpp.add_event_handler('disconnected', self.on_disconnected)
        self.xmpp.add_event_handler('stream_error', self.on_stream_error)
        self.xmpp.add_event_handler('failed_all_auth', self.on_failed_all_auth)
        self.xmpp.add_event_handler('no_auth', self.on_no_auth)
        self.xmpp.add_event_handler("session_start", self.on_session_start)
        self.xmpp.add_event_handler("session_start",
                                    self.on_session_start_features)
        self.xmpp.add_event_handler("groupchat_presence",
                                    self.on_groupchat_presence)
        self.xmpp.add_event_handler("groupchat_message",
                                    self.on_groupchat_message)
        self.xmpp.add_event_handler("groupchat_invite",
                                    self.on_groupchat_invitation)
        self.xmpp.add_event_handler("groupchat_direct_invite",
                                    self.on_groupchat_direct_invitation)
        self.xmpp.add_event_handler("groupchat_decline",
                                    self.on_groupchat_decline)
        self.xmpp.add_event_handler("groupchat_config_status",
                                    self.on_status_codes)
        self.xmpp.add_event_handler("groupchat_subject",
                                    self.on_groupchat_subject)
        self.xmpp.add_event_handler("message", self.on_message)
        self.xmpp.add_event_handler("message_error", self.on_error_message)
        self.xmpp.add_event_handler("receipt_received", self.on_receipt)
        self.xmpp.add_event_handler("got_online", self.on_got_online)
        self.xmpp.add_event_handler("got_offline", self.on_got_offline)
        self.xmpp.add_event_handler("roster_update", self.on_roster_update)
        self.xmpp.add_event_handler("changed_status", self.on_presence)
        self.xmpp.add_event_handler("presence_error", self.on_presence_error)
        self.xmpp.add_event_handler("roster_subscription_request",
                                    self.on_subscription_request)
        self.xmpp.add_event_handler("roster_subscription_authorized",
                                    self.on_subscription_authorized)
        self.xmpp.add_event_handler("roster_subscription_remove",
                                    self.on_subscription_remove)
        self.xmpp.add_event_handler("roster_subscription_removed",
                                    self.on_subscription_removed)
        self.xmpp.add_event_handler("message_xform", self.on_data_form)
        self.xmpp.add_event_handler("chatstate_active",
                                    self.on_chatstate_active)
        self.xmpp.add_event_handler("chatstate_composing",
                                    self.on_chatstate_composing)
        self.xmpp.add_event_handler("chatstate_paused",
                                    self.on_chatstate_paused)
        self.xmpp.add_event_handler("chatstate_gone",
                                    self.on_chatstate_gone)
        self.xmpp.add_event_handler("chatstate_inactive",
                                    self.on_chatstate_inactive)
        self.xmpp.add_event_handler("attention", self.on_attention)
        self.xmpp.add_event_handler("ssl_cert", self.validate_ssl)
        self.xmpp.add_event_handler("ssl_invalid_chain", self.ssl_invalid_chain)
        self.all_stanzas = Callback('custom matcher',
                                    connection.MatchAll(None),
                                    self.incoming_stanza)
        self.xmpp.register_handler(self.all_stanzas)
        if config.get('enable_user_tune'):
            self.xmpp.add_event_handler("user_tune_publish",
                                        self.on_tune_event)
        if config.get('enable_user_nick'):
            self.xmpp.add_event_handler("user_nick_publish",
                                        self.on_nick_received)
        if config.get('enable_user_mood'):
            self.xmpp.add_event_handler("user_mood_publish",
                                        self.on_mood_event)
        if config.get('enable_user_activity'):
            self.xmpp.add_event_handler("user_activity_publish",
                                        self.on_activity_event)
        if config.get('enable_user_gaming'):
            self.xmpp.add_event_handler("user_gaming_publish",
                                        self.on_gaming_event)


    on_session_start_features = handlers.on_session_start_features
    on_carbon_received = handlers.on_carbon_received
    on_carbon_sent = handlers.on_carbon_sent
    on_groupchat_invitation = handlers.on_groupchat_invitation
    on_groupchat_direct_invitation = handlers.on_groupchat_direct_invitation
    on_groupchat_decline = handlers.on_groupchat_decline
    on_message = handlers.on_message
    on_error_message = handlers.on_error_message
    on_normal_message = handlers.on_normal_message
    on_nick_received = handlers.on_nick_received
    on_gaming_event = handlers.on_gaming_event
    on_mood_event = handlers.on_mood_event
    on_activity_event = handlers.on_activity_event
    on_tune_event = handlers.on_tune_event
    on_groupchat_message = handlers.on_groupchat_message
    on_muc_own_nickchange = handlers.on_muc_own_nickchange
    on_groupchat_private_message = handlers.on_groupchat_private_message
    on_chatstate_active = handlers.on_chatstate_active
    on_chatstate_inactive = handlers.on_chatstate_inactive
    on_chatstate_composing = handlers.on_chatstate_composing
    on_chatstate_paused = handlers.on_chatstate_paused
    on_chatstate_gone = handlers.on_chatstate_gone
    on_chatstate = handlers.on_chatstate
    on_chatstate_normal_conversation = handlers.on_chatstate_normal_conversation
    on_chatstate_private_conversation = \
            handlers.on_chatstate_private_conversation
    on_chatstate_groupchat_conversation = \
            handlers.on_chatstate_groupchat_conversation
    on_roster_update = handlers.on_roster_update
    on_subscription_request = handlers.on_subscription_request
    on_subscription_authorized = handlers.on_subscription_authorized
    on_subscription_remove = handlers.on_subscription_remove
    on_subscription_removed = handlers.on_subscription_removed
    on_presence = handlers.on_presence
    on_presence_error = handlers.on_presence_error
    on_got_offline = handlers.on_got_offline
    on_got_online = handlers.on_got_online
    on_groupchat_presence = handlers.on_groupchat_presence
    on_failed_connection = handlers.on_failed_connection
    on_disconnected = handlers.on_disconnected
    on_stream_error = handlers.on_stream_error
    on_failed_all_auth = handlers.on_failed_all_auth
    on_no_auth = handlers.on_no_auth
    on_connected = handlers.on_connected
    on_connecting = handlers.on_connecting
    on_session_start = handlers.on_session_start
    on_status_codes = handlers.on_status_codes
    on_groupchat_subject = handlers.on_groupchat_subject
    on_data_form = handlers.on_data_form
    on_receipt = handlers.on_receipt
    on_attention = handlers.on_attention
    room_error = handlers.room_error
    check_bookmark_storage = handlers.check_bookmark_storage
    outgoing_stanza = handlers.outgoing_stanza
    incoming_stanza = handlers.incoming_stanza
    validate_ssl = handlers.validate_ssl
    ssl_invalid_chain = handlers.ssl_invalid_chain
    on_next_adhoc_step = handlers.on_next_adhoc_step
    on_adhoc_error = handlers.on_adhoc_error
    cancel_adhoc_command = handlers.cancel_adhoc_command
    validate_adhoc_step = handlers.validate_adhoc_step
    terminate_adhoc_command = handlers.terminate_adhoc_command

class ConfigurationHandler(object):
    def __init__(self):
        # a dict of the form {'config_option': [list, of, callbacks]}
        # Whenever a configuration option is changed (using /set or by
        # reloading a new config using a signal), all the associated
        # callbacks are triggered.
        # Use Core.add_configuration_handler("option", callback) to add a
        # handler
        # Note that the callback will be called when it’s changed in the
        # global section, OR in a special section.
        # As a special case, handlers can be associated with the empty
        # string option (""), they will be called for every option change
        # The callback takes two argument: the config option, and the new
        # value
        self.configuration_change_handlers = {"": []}
        self.add_configuration_handler("create_gaps",
                                       self.on_gaps_config_change)
        self.add_configuration_handler("request_message_receipts",
                                       self.on_request_receipts_config_change)
        self.add_configuration_handler("ack_message_receipts",
                                       self.on_ack_receipts_config_change)
        self.add_configuration_handler("plugins_dir",
                                       self.on_plugins_dir_config_change)
        self.add_configuration_handler("plugins_conf_dir",
                                       self.on_plugins_conf_dir_config_change)
        self.add_configuration_handler("connection_timeout_delay",
                                       self.xmpp.set_keepalive_values)
        self.add_configuration_handler("connection_check_interval",
                                       self.xmpp.set_keepalive_values)
        self.add_configuration_handler("themes_dir",
                                       theming.update_themes_dir)
        self.add_configuration_handler("theme",
                                       self.on_theme_config_change)
        self.add_configuration_handler("use_bookmarks_method",
                                       self.on_bookmarks_method_config_change)
        self.add_configuration_handler("password",
                                       self.on_password_change)
        self.add_configuration_handler("enable_vertical_tab_list",
                                       self.on_vertical_tab_list_config_change)
        self.add_configuration_handler("deterministic_nick_colors",
                                       self.on_nick_determinism_changed)

        self.add_configuration_handler("", self.on_any_config_change)

    def on_any_config_change(self, option, value):
        """
        Update the roster, in case a roster option changed.
        """
        roster.modified()

    def add_configuration_handler(self, option, callback):
        """
        Add a callback, associated with the given option. It will be called
        each time the configuration option is changed using /set or by
        reloading the configuration with a signal
        """
        if option not in self.configuration_change_handlers:
            self.configuration_change_handlers[option] = []
        self.configuration_change_handlers[option].append(callback)

    def trigger_configuration_change(self, option, value):
        """
        Triggers all the handlers associated with the given configuration
        option
        """
        # First call the callbacks associated with any configuration change
        for callback in self.configuration_change_handlers[""]:
            callback(option, value)
        # and then the callbacks associated with this specific option, if
        # any
        if option not in self.configuration_change_handlers:
            return
        for callback in self.configuration_change_handlers[option]:
            callback(option, value)

    def on_bookmarks_method_config_change(self, option, value):
        """
        Called when the use_bookmarks_method option changes
        """
        if value not in ('pep', 'privatexml'):
            return
        self.bookmarks.preferred = value
        self.bookmarks.save(self.xmpp, core=self)

    def on_gaps_config_change(self, option, value):
        """
        Called when the option create_gaps is changed.
        Remove all gaptabs if switching from gaps to nogaps.
        """
        if value.lower() == "false":
            self.tabs = list(tab for tab in self.tabs if tab)

    def on_request_receipts_config_change(self, option, value):
        """
        Called when the request_message_receipts option changes
        """
        self.xmpp.plugin['xep_0184'].auto_request = config.get(option,
                                                               default=True)

    def on_ack_receipts_config_change(self, option, value):
        """
        Called when the ack_message_receipts option changes
        """
        self.xmpp.plugin['xep_0184'].auto_ack = config.get(option, default=True)

    def on_plugins_dir_config_change(self, option, value):
        """
        Called when the plugins_dir option is changed
        """
        path = os.path.expanduser(value)
        self.plugin_manager.on_plugins_dir_change(path)

    def on_vertical_tab_list_config_change(self, option, value):
        """
        Called when the enable_vertical_tab_list option is changed
        """
        self.call_for_resize()

    def on_plugins_conf_dir_config_change(self, option, value):
        """
        Called when the plugins_conf_dir option is changed
        """
        path = os.path.expanduser(value)
        self.plugin_manager.on_plugins_conf_dir_change(path)

    def on_theme_config_change(self, option, value):
        """
        Called when the theme option is changed
        """
        error_msg = theming.reload_theme()
        if error_msg:
            self.information(error_msg, 'Warning')
        self.refresh_window()

    def on_password_change(self, option, value):
        """
        Set the new password in the slixmpp.ClientXMPP object
        """
        self.xmpp.password = value


    def on_nick_determinism_changed(self, option, value):
        """If we change the value to true, we call /recolor on all the MucTabs, to
        make the current nick colors reflect their deterministic value.
        """
        if value.lower() == "true":
            for tab in self.get_tabs(tabs.MucTab):
                tab.command_recolor('')

    def reload_config(self):
        # reload all log files
        log.debug("Reloading the log files…")
        logger.reload_all()
        log.debug("Log files reloaded.")
        # reload the theme
        log.debug("Reloading the theme…")
        theming.reload_theme()
        log.debug("Theme reloaded.")
        # reload the config from the disk
        log.debug("Reloading the config…")
        # Copy the old config in a dict
        old_config = config.to_dict()
        config.read_file()
        # Compare old and current config, to trigger the callbacks of all
        # modified options
        for section in config.sections():
            old_section = old_config.get(section, {})
            for option in config.options(section):
                old_value = old_section.get(option)
                new_value = config.get(option, default="", section=section)
                if new_value != old_value:
                    self.trigger_configuration_change(option, new_value)
        log.debug("Config reloaded.")
        # in case some roster options have changed
        roster.modified()


