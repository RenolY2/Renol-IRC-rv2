from abc import ABC, abstractmethod

class IRCModule(ABC):
    def __init__(self, bot):
        self.bot = bot

        self.set_message_handlers(self.bot.message_handler.set_handler)

    @abstractmethod
    def set_message_handlers(self, set_handler):
        pass
