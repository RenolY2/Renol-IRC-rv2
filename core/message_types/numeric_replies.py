# Here we define the names of the numeric replies.
# The names of the numeric replies are taken
# from the RFC 1459.

class Reply(object):
    # Error replies
    ERR_NO_SUCH_NICK = 401
    ERR_NO_SUCH_SERVER = 402
    ERR_NO_SUCH_CHANNEL = 403
    ERR_CANNOT_SEND_TO_CHAN = 404
    ERR_TOO_MANY_CHANNELS = 405
    ERR_WAS_NO_SUCH_NICK = 406 # Returned by WHOWAS
    ERR_TOO_MANY_TARGETS = 407
    ERR_NO_ORIGIN = 409
    ERR_NO_RECIPIENT = 411
    ERR_NO_TEXT_TO_SEND = 412
    ERR_NO_TOP_LEVEL = 413
    ERR_WILDCARD_IN_TOP_LEVEL = 414

    ERR_UNKNOWN_COMMAND = 421
    ERR_NO_MOTD = 422
    ERR_NO_ADMIN_INFO = 423
    ERR_FILE_ERROR = 424

    ERR_NO_NICKNAME_GIVEN = 431
    ERR_INVALID_NICKNAME = 432
    ERR_NICKNAME_IN_USE = 433
    ERR_NICK_COLLISION = 436

    ERR_USER_NOT_IN_CHANNEL = 441
    ERR_NOT_ON_CHANNEL = 442
    ERR_USER_ALREADY_ON_CHANNEL = 443
    ERR_NO_LOGIN = 444
    ERR_SUMMON_DISABLED = 445
    ERR_USERS_DISABLED = 446

    ERR_NOT_REGISTERED = 451

    ERR_NEED_MORE_PARAMS = 461
    ERR_ALREADY_REGISTERED = 462
    ERR_NO_PERM_FOR_HOST = 463
    ERR_INCORRECT_PASSWORD = 464
    ERR_YOU_ARE_BANNED = 465
    ERR_KEY_ALREADY_SET = 467

    ERR_CHANNEL_IS_FULL = 471
    ERR_CHANNEL_MODE_UNKNOWN_FLAG = 472
    ERR_INVITEONLY_CHAN = 473
    ERR_BANNED_FROM_CHAN = 474
    ERR_BAD_CHANNEL_KEY = 475

    ERR_NO_PRIVILEGES = 481
    ERR_CHAN_OP_PRIVILEGE_NEEDED = 482
    ERR_CANT_KILL_SERVER = 483

    ERR_NO_OPER_HOST = 491

    ERR_USER_MODE_UNKNOWN_FLAG = 501
    ERR_USERS_DONT_MATCH = 502


_reply_names = {}
for key in Reply.__dict__:
    val = Reply.__dict__[key]

    assert val not in _reply_names
    _reply_names[val] = key

def get_reply_name(num):
    return _reply_names[num]

if __name__ == "__main__":
    print(Reply.ERR_NOOPERHOST)
    print(get_reply_name(Reply.ERR_NOOPERHOST))