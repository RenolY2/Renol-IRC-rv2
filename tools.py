from core.helper_functions import choose_casemapping_func

class Tools(object):
    # Functions for converting a name to lower case/upper case
    # according to specific rules, e.g. rfc1459.
    name_lower, name_upper = None, None

    def __init__(self, casemap_default = "rfc1459"):
        name_lower, name_upper = choose_casemapping_func(casemap_default)

    def set_casemap(self, casemap):
        self.name_lower, self.name_upper = choose_casemapping_func(casemap)
