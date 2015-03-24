from abc import ABC, abstractmethod

class IRCModule(ABC):

    @abstractmethod
    def set_message_handlers(self, set_handler):
        pass
