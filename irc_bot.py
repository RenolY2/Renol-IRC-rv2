import time
import logging
from collections import OrderedDict

from core.networking import Networking
from core.message_types.message_handler import MessageHandler
from configuration import Config

from core.message_types.server_information import ServerInformation
from core.message_types.user_messages import UserMessages
from core.message_types.channel_manager import ChannelManager

from core.logging import setup_logging

from misc.config_templates import default_bot_config
from tools import Tools


class IRCBot(object):
    def __init__(self, bot_config):
        self.bot_config = bot_config

        setup_logging(loglevel="INFO", console_loglevel="DEBUG",
                      log_path_format="logs/botlogs/%Y/%m/%Y-%m-%d.log")

        self.log = logging.getLogger("bot")

        conninfo = self.bot_config["Connection Info"]
        self.irc_networking = Networking(conninfo["host"],
                                         conninfo["port"],
                                         timeout=conninfo["timeout"])

        msginfo = self.bot_config["Bot Options"]["Message Sending"]
        self.irc_networking.set_wait_coefficient(base_delay=msginfo["minimum delay"],
                                                 messages_per_minute=msginfo["messages per minute"],
                                                 burst=msginfo["burst"])

        self.message_handler = MessageHandler()

        self.user_messages = UserMessages(self)
        self.server_info = ServerInformation(self)
        self.channel_manager = ChannelManager(self)

        self.tools = Tools()

        self.log.info("All modules configured and set up. Bot is ready to go.")

        self._shutdown = False

    def start(self):
        userinfo = self.bot_config["User Info"]
        conninfo = self.bot_config["Connection Info"]

        self.irc_networking.start_threads()

        self.irc_networking.send_msg("PASS", [userinfo["password"]])
        self.irc_networking.send_msg("NICK", [userinfo["name"]])
        self.irc_networking.send_msg("USER", [userinfo["ident"], "*", "*"], userinfo["realname"])

        self.log.info("User info sent to server. Bot name: %s, identity: %s, real name: %s",
                      userinfo["name"], userinfo["ident"], userinfo["realname"])
        self.log.info("Listening for incoming messages now.")

        last_ping = time.time()

        while not self._shutdown:
            msg = self.irc_networking.read_msg()
            if msg is None:
                time.sleep(0.1)
            else:
                pref, cmd, args, text = msg
                #print(msg)
                if cmd == "PING":
                    self.irc_networking.send_msg("PONG", message=text)

                if self.message_handler.has_handler(cmd):
                    self.message_handler.execute_handler(cmd,
                                                         self, cmd, pref, args, text)

                if cmd == "376":
                    #self.irc_networking.send_msg("JOIN", self.bot_config["Connection Info"]["channels"])
                    #self.log.info("Joining channels: %s",
                    #              ", ".join(self.bot_config["Connection Info"]["channels"]))
                    #self.channel_manager.join_channel(*[("#"+"a"*40+str(x)) for x in range(25)])
                    self.channel_manager.join_channel(*self.bot_config["Connection Info"]["channels"])
            """
            if (time.time() - last_ping) > 30:
                IRCNetworking.send_msg("PING", [host])
                last_ping = time.time()
            """
            if self.irc_networking.thread_has_crashed:
                self.shutdown_bot()

    def shutdown_bot(self):
        self.irc_networking.send_msg("QUIT", ["Test"])#message="Shutting down")
        self._shutdown = True

if __name__ == "__main__":
    bot_config = Config("config.yaml", schema=default_bot_config)
    bot_config.load_file()

    bot = IRCBot(bot_config)
    bot.start()

    log = logging.getLogger("bot.shutdown")
    log.info("Now shutting down.")

    # Wait until all outgoing messages have been sent.
    # This allows the quit message to be received by the server before the connection is cut.

    log.info("Status of send queue: Empty:%s/Full:%s",
             bot.irc_networking.send_thread._buffer.empty(),
             bot.irc_networking.send_thread._buffer.full())

    log.info("Status of read queue: Empty:%s/Full:%s",
             bot.irc_networking.read_thread._buffer.empty(),
             bot.irc_networking.read_thread._buffer.full())

    bot.irc_networking.wait()

    logging.shutdown()

    log.info("Shut down!")