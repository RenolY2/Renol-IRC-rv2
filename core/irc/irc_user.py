from irc_target import IRC_Target


class User(IRC_Target):
    rank_symbol = ""
    rank = 0

    # The ident and hostname of an user is not when a channel
    # is first joined. This information needs to be added
    # at a later time, e.g. by sending a WHO command with
    # the channel name to the server
    identity = None
    hostname = None

    def __init__(self, bot_cls, name):
        super(User, self).__init__(bot_cls, name)


    def _change_rank(self, rank_symbol, rank_number):
        self.rank_symbol = rank_symbol
        self.rank = rank_number

    def _change_nick(self, nickname):
        self.name = nickname