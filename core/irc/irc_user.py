from irc_target import IRC_Target


class User(IRC_Target):
    rank_symbol = ""
    rank = 0

    def __init__(self, bot_cls, name):
        super(User, self).__init__(bot_cls, name)

    def _change_rank(self, rank_symbol, rank_number):
        self.rank_symbol = rank_symbol
        self.rank = rank_number