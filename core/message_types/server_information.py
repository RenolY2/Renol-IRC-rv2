from .irc_module_template import IRCModule
from .numeric_replies import Reply


class ServerInformation(IRCModule):
    isupport = {}

    #def __init__(self):
    #    pass


    def handle_isupport_reply(self, bot,
                              cmd, pref, args, text):
        if len(args) >= 2:
            nickname = args[0]
            tokens = args[1:]

            for token in tokens:
                # According to the draft of the RPL_ISUPPORT reply,
                # a token of the form 'name' is considered equivalent
                # to 'name=', i.e. a token with an empty value.
                # partition() will return an empty value on both
                # forms, therefore it is suited for parsing the tokens.
                token_name, sep, value = token.partition("=")

                self.isupport[token_name] = value

                if token_name == "CASEMAPPING":
                    bot.tools.set_casemap(value)
                if token_name == "CHANNELLEN":
                    self.isupport[token_name] = int(value)


    def set_message_handlers(self, set_handler):
        set_handler(Reply.RPL_ISUPPORT, self.handle_isupport_reply)
