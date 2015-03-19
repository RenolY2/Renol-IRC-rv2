import time
from collections import OrderedDict

from core.networking import Networking
from configuration import Config
from misc.config_templates import default_bot_config

ConfigSchema = Config(default_bot_config)
with open("config.yaml", "r") as f:
    config = ConfigSchema.load_file(f)

userinfo = config["User Info"]
conninfo = config["Connection Info"]

IRCNetworking = Networking(conninfo["host"], conninfo["port"], timeout=300)
IRCNetworking.start_threads()

IRCNetworking.send_msg("PASS", [userinfo["password"]])
IRCNetworking.send_msg("NICK", [userinfo["name"]])
IRCNetworking.send_msg("USER", [userinfo["ident"], "*", "*"], userinfo["realname"])

print("Read loop starting now!")

last_ping = time.time()
running = True

while running:
    msg = IRCNetworking.read_msg()
    if msg is None:
        time.sleep(0.1)
    else:
        pref, cmd, args, text = msg
        print(msg)
        if cmd == "PING":
            IRCNetworking.send_msg("PONG", message=text)
        if cmd == "004":
            IRCNetworking.send_msg("JOIN", ["#test"])
    """
    if (time.time() - last_ping) > 30:
        IRCNetworking.send_msg("PING", [host])
        last_ping = time.time()
    """
    if IRCNetworking.thread_has_crashed:
        running = False
