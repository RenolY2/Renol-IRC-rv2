import logging

from .irc_module_template import IRCModule
from .numeric_replies import Reply


class UserMessages(IRCModule):
    def __init__(self):
        self.log = logging.getLogger("bot.")

    def privmsg_handler(self, bot,
                        cmd, pref, args, text):
        channel = args[0]
        if "lowercase" in text:
            name, sep, rest = pref.partition("!")
            ident, sep, host = rest.partition("@")


            bot.irc_networking.send_msg("PRIVMSG", [channel],
                                        "Uppercase: {0}, lowercase: {1}".format(
                                            bot.tools.name_upper(name),
                                            bot.tools.name_lower(name)
                                        ))
        elif text.startswith("say "):
            start, rest = text.split("say ", 1)
            bot.irc_networking.send_msg("PRIVMSG", [channel], rest+" ")

            if "debug" in text:
                self.log.debug("Message was logged as debug from %s: %s",
                               name, text)
            else:
                self.log.info("Message was logged as info from %s: %s",
                               name, text)

        elif text.startswith("shutdown"):
            raise RuntimeError("Shutting down")

        elif text.startswith("flood_test"):
            #raise RuntimeError("Shutting down")
            for i in range(15):
                bot.irc_networking.send_msg("PRIVMSG", [channel], "Test {0}".format(i))


    def set_message_handlers(self, set_handler):
        set_handler("PRIVMSG", self.privmsg_handler)