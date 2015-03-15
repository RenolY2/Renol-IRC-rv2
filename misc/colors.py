""" This is a full mIRC standard color library.
    (It also includes format standards introduced by mIRC.)
"""

__author__ = "DarkMio"
__builtins__ = None


__bold__           = chr(2)
__italic__         = chr(9)
__strike_through__ = chr(19)
__reset__          = chr(15)
__underline__      = chr(21)
__underline2__     = chr(31)
__reverse__        = chr(22)
__color__          = chr(3)

black      = "1"
navy_blue  = "2"
green      = "3"
red        = "4"
brown      = "5"
purple     = "6"
olive      = "7"
yellow     = "8"
lime_green = "9"
teal       = "10"
aqua_light = "11"
royal_blue = "12"
hot_pint   = "13"
dark_gray  = "14"
light_gray = "15"
white      = "16"


def color(foreground, background=None):
    if background:
        background = ",{}".format(background)
    else:
        background = ""
    return "{control}{color}{background}".format(control=__color__, color=foreground, background=background)