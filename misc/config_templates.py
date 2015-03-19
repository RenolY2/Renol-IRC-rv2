from collections import OrderedDict

_user_info = OrderedDict([
    ("password", "abc"),
    ("name", "MyNickname"),
    ("ident", "RenolIRCBot"),
    ("realname", "RenolIRCBot"),
])

_connection_info = OrderedDict([
    ("host", ""),
    ("port", 6667),
    ("bind address", ["", 0]),
    ("timeout", 300)
])

default_bot_config = OrderedDict([
    ("User Info", _user_info),
    ("Connection Info", _connection_info)
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