

class UserNotInChannelError(Exception):
    def __init__(self, name, name_lowercase, channel_name):
        self.name_lowercase = name_lowercase
        self.name = name
        self.channel_name = channel_name

    def __str__(self):
        return ("User '{name}'(lower case: {name_lower}) "
                "doesn't exist in channel '{chan}'".format(
                    name=self.name, name_lower=self.name_lowercase,
                    chan=self.channel_name
                    )
        )


class UserAlreadyInChannelError(Exception):
    def __init__(self, name, name_lowercase, channel_name):
        self.name_lowercase = name_lowercase
        self.name = name
        self.channel_name = channel_name

    def __str__(self):
        return ("User '{name}'(lower case: {name_lower}) "
                "already exists in channel '{chan}'".format(
                    name=self.name, name_lower=self.name_lowercase,
                    chan=self.channel_name
                    )
        )


# An IRC target is an entity to which a private message can be sent.
# The only IRC targets, as of now, are the IRC user and the IRC channel.
class IRCTarget(object):
    def __init__(self, name):
        self.name = name



class User(IRCTarget):
    # The irc server can set various flags on the user that
    # highlight his abilities.
    flags = {}

    # The ident and hostname of an user is not known when a channel
    # is first joined. This information needs to be added
    # at a later time, e.g. by sending a WHO command and parsing the response.
    identity = None
    hostname = None

    authed = False

    def __init__(self, name):
        super().__init__(name)


class Channel(IRCTarget):
    topic = ""
    userlist = {}

    def __init__(self, name, lowercase_func, uppercase_func):
        super().__init__(name)

        self._lowercase_func = lowercase_func
        self._uppercase_func = uppercase_func

    def set_topic(self, topic):
        pass

    # Add the user to the channel's userlist. The user must not exist yet.
    def add_user(self, name, user_obj):
        name_lower = self._lowercase_func(name)

        if name_lower in self.userlist:
            raise UserAlreadyInChannelError(name, name_lower, channel_name=self.name)

        self.userlist[name_lower] = user_obj

    # Remove the user from the channel's userlist. The user must exist.
    def remove_user(self, name):
        name_lower = self._lowercase_func(name)

        try:
            del self.userlist[name_lower]
        except KeyError:
            raise UserNotInChannelError(name, name_lower, channel_name=self.name)

    # Retrieve the user from the channel's userlist. The user must exist.
    def get_user(self, name):
        name_lower = self._lowercase_func(name)

        try:
            return self.userlist[name_lower]
        except KeyError:
            raise UserNotInChannelError(name, name_lower, channel_name=self.name)

    def user_exists(self, name):
        name_lower = self._lowercase_func(name)

        return name_lower in self.userlist