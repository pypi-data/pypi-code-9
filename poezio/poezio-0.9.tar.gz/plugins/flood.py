from plugin import BasePlugin
import tabs
import multiuserchat as muc

class Plugin(BasePlugin):
    def init(self):
        self.add_tab_command(tabs.MucTab, 'flood', self.command_flood, 'Test command')
        self.add_tab_command(tabs.MucTab, 'boom', self.command_boom, 'Test command')
        self.add_tab_command(tabs.MucTab, 'pres', self.command_pres, 'Test command')

    def command_flood(self, args):
        tab = self.api.current_tab()
        for i in range(int(args.strip())):
            tab.command_say('toto %s' % i)

    def command_boom(self, args):
        tab = self.api.current_tab()
        for i in range(int(args.strip())):
            tab.command_correct('coucou %s' % i)

    def command_pres(self, args):
        tab = self.api.current_tab()
        for i in range(int(args.strip())):
            muc.change_show(self.core.xmpp, tab.name, tab.own_nick, 'away', 'coucou1')
            muc.change_show(self.core.xmpp, tab.name, tab.own_nick, 'available', 'coucou2')

