

# The MessageHandler class allows one handler to
# be registered for each type of message. As such,
# it is slightly different from
class MessageHandler(object):
    _handler = {}

    def __init__(self):
        pass

    def set_handler(self, message_name, handler):
        assert isinstance(message_name, str)
        assert message_name not in self._handler
        assert callable(handler)

        self._handler[message_name] = handler

    def remove_handler(self, message_name):
        del self._handler[message_name]

    def has_handler(self, message_name):
        return message_name in self._handler

    def execute_handler(self, message_name, *args, **kwargs):
        self._handler[message_name](*args, **kwargs)