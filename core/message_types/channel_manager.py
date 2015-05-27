import logging

from core.irc.irc_targets import Channel
from core.datatypes.custom_collections import NormalizedDict

from .irc_module_template import IRCModule
from .numeric_replies import Reply



class ChannelError(Exception):
    def __init__(self, channel_name):
        self.channel_name = channel_name

class InvalidChannelError(ChannelError):
    def __str__(self):
        return "Invalid channel name: '{0}'".format(self.channel_name)

class ChannelAlreadyJoinedError(ChannelError):
    def __str__(self):
        return "Channel already joined: '{0}'".format(self.channel_name)

class ChannelNameTooLongError(ChannelError):
    def __init__(self, channel_name, limit):
        super().__init__(self, channel_name)
        self.chan_limit = limit


    def __str__(self):
        return ("Channel name too long: '{0}' "
                "({1} characters, limit is {2})".format(self.channel_name,
                                                        len(self.channel_name),
                                                        self.chan_limit)
        )

class ChannelManager(IRCModule):
    def __init__(self, bot):
        super().__init__(bot)

        # Because channel names are case insensitive, we will use our NormalizedDict class
        # with the str.lower function to make all keys lowercase before operating on them.
        self.channels = NormalizedDict(normalize_func=str.lower)

    def set_message_handlers(self, set_handler):
        pass

    def _validate_name(self, channel_name):

        # Empty strings and strings with spaces are not valid
        # channel names.
        if len(channel_name) == 0 or " " in channel_name:
            raise InvalidChannelError(channel_name)

        if channel_name in self.channels:
            raise ChannelAlreadyJoinedError(channel_name)

        isupport = self.bot.server_info.isupport
        chan_type = channel_name[0]

        # If the channel type is not supported by the server, or the channel
        # type isn't valid, then the channel name isn't valid.
        if chan_type not in isupport["CHANTYPES"]:
            raise InvalidChannelError(channel_name)

        if len(channel_name) > isupport["CHANNELLEN"]:
            raise ChannelNameTooLongError(channel_name, isupport["CHANNELLEN"])

    def join_channel(self, *channels):
        lowercase_func = self.bot.tools.name_lower
        uppercase_func = self.bot.tools.name_upper

        for channel_name in channels:
            self._validate_name(channel_name)

            channel = Channel(channel_name,
                              lowercase_func, uppercase_func)

            self.channels[channel_name] = channel

        partitions = self.bot.irc_networking.send_thread.partition_arguments(channels)

        for arguments in partitions:
            self.bot.irc_networking.send_msg("JOIN", arguments=arguments)
