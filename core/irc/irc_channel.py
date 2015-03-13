from irc_target import IRC_Target

class Channel(IRC_Target):
    topic = ""
    def __init__(self, bot_cls, name):
        super(Channel, self).__init__(bot_cls, name)


    def _set_topic(self, topic):
        pass
