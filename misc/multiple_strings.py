"""Helps with english. If the word has a form of multiple, you can feed it's value
   and it returns you the appropiate form. (Also has some extra features, in case you have a collection of strings.)"""


def multiple_of(value, string_of_single, string_of_multiple, return_with_value=False, before_string=None, after_string=None):
    cache = ''
    if not before_string:
        before_string = ''
    if not after_string:
        after_string = ''

    cache += before_string

    if return_with_value:
        cache += str(value) + " "
    if value == 0:
        return
    if value == 1:
        return cache + string_of_single + after_string
    return cache + string_of_multiple + after_string


if __name__ == "__main__":
    print(multiple_of(1, "shoe", "shoes"))
    print(multiple_of(0, "shoe", "shoes"))
    print(multiple_of(10, "shoe", "shoes", False))
    print(multiple_of(10, "shoe", "shoes", True))
    print(multiple_of(10, "shoe", "shoes", True, "!> "))
    print(multiple_of(10, "shoe", "shoes", True, "!> ", ","), multiple_of(10, "shoe", "shoes", True, "!> ", ","))
    print(multiple_of(10, "shoe", "shoes", False, after_string=", "))