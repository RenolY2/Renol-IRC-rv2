from collections import OrderedDict

_user_info = OrderedDict([
    ("password", "abc"),
    ("name", "MyNickname"),
    ("ident", "RenolIRCBot"),
    ("realname", "RenolIRCBot")
])

_connection_info = OrderedDict([
    ("host", ""),
    ("port", 6667),
    ("bind address", ["", 0]),
    ("timeout", 300),
    ("channels", [])
])

_message_sending = OrderedDict([
    ("minimum delay", 2.0),

    # This has an effect on how quickly the message
    # delay rises for each message sent.
    # A lower number means that the delay rises quicker,
    # but the maximum delay will always be 2 seconds.
    ("messages per minute", 30),

    # This is for how many messages the minimum delay
    # should be kept.
    ("burst", 0)
])

_bot_options = OrderedDict([
    ("Message Sending", _message_sending)
])

default_bot_config = OrderedDict([
    ("User Info", _user_info),
    ("Connection Info", _connection_info),
    ("Bot Options", _bot_options)
])
"""default_bot_config = {
    "User Info": {
        "nickname": "MyNickname",
        "ident": "RenolIRCBot",
        "realname": "RenolIRCBot",
        "password": "abc"
    },
    "Connection Info": {
        "host": "",
        "port": 6667,
        "bind address": ["", 0],
        "timeout": 240
    }

}"""