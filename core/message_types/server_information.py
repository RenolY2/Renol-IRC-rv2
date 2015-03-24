from .irc_module_template import IRCModule
from .numeric_replies import Reply


class ServerInformation(IRCModule):
    def __init__(self):
        pass


    def handle_isupport_reply(self, bot,
                              cmd, pref, args, text):
        print("RECEIVED ISUPPORT")

    def set_message_handlers(self, set_handler):
        set_handler(Reply.ISUPPORT, self.handle_isupport_reply)