

# According to the RFC 1459, {,} and | are the lower case variants of
# the characters [,] and /, respectively.
LOWERCASE_TRANS = str.maketrans("[]\\", "{}|")
UPPERCASE_TRANS = str.maketrans("{}|", "[]\\")


def lowercase_rfc1459(name):
    name_lower = name.lower()
    return name_lower.translate(LOWERCASE_TRANS)
def uppercase_rfc1459(name):
    name_upper = name.upper()
    return name_upper.translate(UPPERCASE_TRANS)

def uppercase_default(name):
    return name.upper()
def lowercase_default(name):
    return name.lower()


def choose_casemapping_func(casemap):
    casemap_funcs = {"rfc1459": (lowercase_rfc1459,
                                  uppercase_rfc1459),
                     "default": (lowercase_default,
                                uppercase_default)}

    if casemap in casemap_funcs:
        return casemap_funcs[casemap]
    else:
        return casemap_funcs["default"]

if __name__ == "__main__":
    lowercase, uppercase = choose_casemapping_func("rfc1459")

    print(lowercase("Bla[]"))
    print(uppercase("Bla[]"))


    lowercase, uppercase = choose_casemapping_func("none")

    print(lowercase("bla[]7"))
    print(uppercase("bla}"))