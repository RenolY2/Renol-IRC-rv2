from irc_target import IRC_Target


class Channel(IRC_Target):
    topic = ""
    userlist = None


    def __init__(self, lowercase_func, bot_cls, name):
        super(Channel, self).__init__(bot_cls, name)
        self.userlist = NormalizedDict(lowercase_func)

    def _set_topic(self, topic):
        pass


class ChannelFactory(object):
    def __init__(self, lowercase):
        self.lowercase = lowercase

    def create_channel(self, bot_cls, name):
        return Channel(self.lowercase, bot_cls, name)





if __name__ == "__main__":
    def lowercase(str):
        return str.lower()

    fact = ChannelFactory(lowercase)
    chan = fact.create_channel(None, "Hello")

    dic = chan.userlist
    dic["HELLO"] = "hi"
    print(dic)
    print("hElLo" in dic)
