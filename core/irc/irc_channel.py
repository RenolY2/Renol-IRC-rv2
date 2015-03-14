from irc_target import IRC_Target
from collections import MutableMapping


class ChannelFactory(object):
    def __init__(self, lowercase):
        self.lowercase = lowercase

    def create_channel(self_, bot_cls, name):

        class NormalizedDict(MutableMapping):
            def __init__(self, *args, **kwargs):
                self.dict = dict()
                self.update(dict(*args, **kwargs))
            def __getitem__(self, item):
                self.dict[self_.lowercase(item)]
            def __setitem__(self, key, value):
                self.dict[self_.lowercase(key)] = value
            def __delitem__(self, key):
                del self.dict[self_.lowercase(key)]
            def __contains__(self, item):
                return self_.lowercase(item) in self.dict
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
            userlist = NormalizedDict()


            def __init__(self_, bot_cls, name):
                super(Channel, self_).__init__(bot_cls, name)


            def _set_topic(self_, topic):
                pass

        return Channel(bot_cls, name)

if __name__ == "__main__":
    def lowercase(str):
        return str.lower()

    fact = ChannelFactory(lowercase)
    chan = fact.create_channel(None, "Hello")

    dic = chan.userlist
    dic["HELLO"] = "hi"
    print(dic)
    print("hElLo" in dic)
