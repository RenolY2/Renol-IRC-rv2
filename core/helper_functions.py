

# According to the RFC 1459, {,} and | are the lower case variants of
# the characters [,] and /, respectively.
STRICT_LOWERCASE_TRANS = str.maketrans("[]\\", "{}|")
STRICT_UPPERCASE_TRANS = str.maketrans("{}|", "[]\\")

# According to http://www.irc.org/tech_docs/005.html there is a less strict
# variant of the casemapping that considers ~ to be the lower case variant of ^.
LOWERCASE_TRANS = str.maketrans("[]\\^", "{}|~")
UPPERCASE_TRANS = str.maketrans("{}|~", "[]\\^")



def lowercase_strict_rfc1459(name):
    name_lower = name.lower()
    return name_lower.translate(STRICT_LOWERCASE_TRANS)
def uppercase_strict_rfc1459(name):
    name_upper = name.upper()
    return name_upper.translate(STRICT_UPPERCASE_TRANS)

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
                                uppercase_default),
                     "strictrfc1459" : (lowercase_strict_rfc1459,
                                        uppercase_strict_rfc1459)}

    if casemap in casemap_funcs:
        return casemap_funcs[casemap]
    else:
        return casemap_funcs["default"]

if __name__ == "__main__":
    lowercase, uppercase = choose_casemapping_func("rfc1459")

    print(lowercase("Bla[]^"))
    print(uppercase("Bla[]~"))

    lowercase, uppercase = choose_casemapping_func("strictrfc1459")
    print(lowercase("BLA[]^^"))


    lowercase, uppercase = choose_casemapping_func("none")

    print(lowercase("bla[]7"))
    print(uppercase("bla}"))