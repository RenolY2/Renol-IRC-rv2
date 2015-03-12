
# Class that covers some aspects used by both an IRC user and an IRC channel.

# According to the RFC 1459, {,} and | are the lower case variants of
# the characters [,] and /, respectively.
LOWERCASE_TRANS = str.maketrans("[]\\", "{}|")
UPPERCASE_TRANS = str.maketrans("{}|", "[]\\")


class IRC_Target(object):
    def __init__(self, bot_cls, name):
        self._bot_cls = bot_cls

        self.name = name

    @property
    def name_lowercase(self):
        name_lower = self.name.lower()
        return name_lower.translate(LOWERCASE_TRANS)





if __name__ == "__main__":
    user1 = IRC_Target(None, "HansMaus12312")
    print(user1.name_lowercase)
    user2 = IRC_Target(None, "IamNotHere[GONE]")
    print(user2.name_lowercase)

    channel = IRC_Target(None, "#BÄSSSß\\")
    print(channel.name_lowercase)
