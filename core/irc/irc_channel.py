from irc_target import IRC_Target
from collections import MutableMapping

class NormalizedDict(MutableMapping):
    def __init__(self, normalize_func, *args, **kwargs):
        self.dict = dict()
        self.update(dict(*args, **kwargs))
        self.norm_func = normalize_func

    def __getitem__(self, item):
        self.dict[self.norm_func(item)]
    def __setitem__(self, key, value):
        self.dict[self.norm_func(key)] = value
    def __delitem__(self, key):
        del self.dict[self.norm_func(key)]
    def __contains__(self, item):
        return self.norm_func(item) in self.dict
    def __iter__(self):
        return iter(self.dict)
    def __len__(self):
        return len(self.dict)
    def __str__(self):
        return str(self.dict)
    def __repr__(self):
        return repr(self.dict)


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
