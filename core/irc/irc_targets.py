
# An IRC target is an entity to which a private message can be sent.
# The only IRC targets, as of now, are the IRC user and the IRC channel.
#
# Some variables are defined as properties. This is so the user won't
# think he can overwrite the variables without side effects.



# Class that covers some aspects used by both an IRC user and an IRC channel.
class IRCTarget(object):
    def __init__(self, name):
        self._name = name

    @property
    def name(self):
        return self._name



class User(IRCTarget):
    # The flag is a symbol that specifies the role
    # of the user, such as having voice or being channel operator.
    _flag = ""

    # The ident and hostname of an user is not known when a channel
    # is first joined. This information needs to be added
    # at a later time, e.g. by sending a WHO command and parsing the response.
    _identity = None
    _hostname = None

    def __init__(self, name):
        super().__init__(name)


    def _change_flag(self, flag):
        self.flag =flag

    def _change_nick(self, nickname):
        self._name = nickname

    @property
    def flag(self):
        return self._flag

    @property
    def identity(self):
        return self._identity

    @property
    def hostname(self):
        return self._hostname


class Channel(IRCTarget):
    _topic = ""
    _userlist = {}

    def __init__(self, name):
        super().__init__(name)

    def _set_topic(self, topic):
        pass

    @property
    def topic(self):
        return self._topic

    @property
    def userlist(self):
        return self._userlist