import time
from collections import OrderedDict

from core.networking import Networking
from configuration import Config
from misc.config_templates import default_bot_config


class IRCBot(object):
    def __init__(self):
        self.bot_config = Config("config.yaml", schema=default_bot_config)
        self.bot_config.load_file()

    def start(self):
        userinfo = self.bot_config["User Info"]
        conninfo = self.bot_config["Connection Info"]

        irc_networking = Networking(conninfo["host"], conninfo["port"], timeout=conninfo["timeout"])
        irc_networking.start_threads()

        irc_networking.send_msg("PASS", [userinfo["password"]])
        irc_networking.send_msg("NICK", [userinfo["name"]])
        irc_networking.send_msg("USER", [userinfo["ident"], "*", "*"], userinfo["realname"])

        print("Read loop starting now!")

        last_ping = time.time()
        running = True

        while running:
            msg = irc_networking.read_msg()
            if msg is None:
                time.sleep(0.1)
            else:
                pref, cmd, args, text = msg
                print(msg)
                if cmd == "PING":
                    irc_networking.send_msg("PONG", message=text)
                if cmd == "004":
                    irc_networking.send_msg("JOIN", ["#test"])
            """
            if (time.time() - last_ping) > 30:
                IRCNetworking.send_msg("PING", [host])
                last_ping = time.time()
            """
            if irc_networking.thread_has_crashed:
                running = False

if __name__ == "__main__":
    bot = IRCBot()
    bot.start()