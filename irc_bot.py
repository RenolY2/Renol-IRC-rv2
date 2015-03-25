import time
from collections import OrderedDict

from core.networking import Networking
from core.message_types.message_handler import MessageHandler
from configuration import Config

from core.message_types.server_information import ServerInformation
from core.message_types.user_messages import UserMessages

from misc.config_templates import default_bot_config
from tools import Tools

class IRCBot(object):
    def __init__(self):
        self.bot_config = Config("config.yaml", schema=default_bot_config)
        self.bot_config.load_file()

        conninfo = self.bot_config["Connection Info"]
        self.irc_networking = Networking(conninfo["host"], conninfo["port"], timeout=conninfo["timeout"])
        self.irc_networking._set_wait_coefficient(base_delay=0.2, messages_per_minute=15, burst=2)

        self._message_handler = MessageHandler()

        self.user_messages = UserMessages()
        self.user_messages.set_message_handlers(self._message_handler.set_handler)

        self.server_info = ServerInformation()
        self.server_info.set_message_handlers(self._message_handler.set_handler)

        self.tools = Tools()

    def start(self):
        userinfo = self.bot_config["User Info"]
        conninfo = self.bot_config["Connection Info"]


        self.irc_networking.start_threads()

        self.irc_networking.send_msg("PASS", [userinfo["password"]])
        self.irc_networking.send_msg("NICK", [userinfo["name"]])
        self.irc_networking.send_msg("USER", [userinfo["ident"], "*", "*"], userinfo["realname"])

        print("Read loop starting now!")

        last_ping = time.time()
        running = True

        while running:
            msg = self.irc_networking.read_msg()
            if msg is None:
                time.sleep(0.1)
            else:
                pref, cmd, args, text = msg
                print(msg)
                if cmd == "PING":
                    self.irc_networking.send_msg("PONG", message=text)
                if cmd == "004":
                    self.irc_networking.send_msg("JOIN", ["#test"])

                if self._message_handler.has_handler(cmd):
                    self._message_handler.execute_handler(cmd,
                                                          self, cmd, pref, args, text)
            """
            if (time.time() - last_ping) > 30:
                IRCNetworking.send_msg("PING", [host])
                last_ping = time.time()
            """
            if self.irc_networking.thread_has_crashed:
                running = False

if __name__ == "__main__":
    bot = IRCBot()
    bot.start()