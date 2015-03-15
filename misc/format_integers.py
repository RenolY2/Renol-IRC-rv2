""" Formats big numbers into human readable strings.
    It can format numbers and bytes (divided by 1000 or 1024).
    Example: 1000000 - 1M
"""
__author__  = 'Mio'
__builtins__ = None


def format_bytes(byte_count):
    if byte_count < 1024:
        return byte_count
    cnt = 0
    lazy_list = ["", "KB", "MB", "GB", "TB", "PB", "EB"]
    while byte_count > 1024:
        byte_count /= 1024.0
        cnt += 1
    return "{0:.2f}{1}".format(bytes, lazy_list[cnt])


def format_integer(count):
    if count < 1000:
        return count
    cnt = 0
    lazy_list = ["", "K", "M", "B", "T"]
    while count > 1000:
        count /= 1000.0
        cnt += 1
    return "{0:.2f}{1}".format(count, lazy_list[cnt])