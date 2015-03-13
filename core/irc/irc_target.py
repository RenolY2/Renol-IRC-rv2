
# Class that covers some aspects used by both an IRC user and an IRC channel.

class IRC_Target(object):
    def __init__(self, bot_cls, name):
        self._bot_cls = bot_cls

        self.name = name

    def send_message(self, msg):
        pass
