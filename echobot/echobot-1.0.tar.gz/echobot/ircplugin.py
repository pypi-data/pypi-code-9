import irc3

@irc3.plugin
class IRCLogger(object):
    def __init__(self, bot):
        self.bot = bot

    @irc3.event(irc3.rfc.PRIVMSG)
    def privmsg(self, mask, event, target, data):
        self.bot.recv_msg(mask, event, target, data)

    @irc3.event(irc3.rfc.JOIN_PART_QUIT)
    def event(self, mask, event, channel, data):
        self.bot.recv_event(mask, event, channel, data)
