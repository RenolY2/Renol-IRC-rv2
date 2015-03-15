import time

from core.networking import Networking

host = "irc.esper.net"
port = 6667

IRCNetworking = Networking(host, port, timeout=300)
IRCNetworking.start_threads()

passw = "abcd_blemo"
name = "Renolv2"
ident = "RenolBot"
realname = "RenolBot"

IRCNetworking.send_msg("PASS", [passw])
IRCNetworking.send_msg("NICK", [name])
IRCNetworking.send_msg("USER", [ident, "*", "*"], realname)

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
