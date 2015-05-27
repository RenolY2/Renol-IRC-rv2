from collections import MutableMapping


# The NormalizedDict type executes a function on the key name
# and uses the return value of that function to access
# an item in the dictionary.
class NormalizedDict(MutableMapping):
    def __init__(self, normalize_func, *args, **kwargs):
        self.norm_func = normalize_func

        self.dict = dict()
        self.update(dict(*args, **kwargs))

    def __getitem__(self, key):
        return self.dict[self.norm_func(key)]
    def __setitem__(self, key, value):
        self.dict[self.norm_func(key)] = value
    def __delitem__(self, key):
        del self.dict[self.norm_func(key)]
    def __contains__(self, key):
        return self.norm_func(key) in self.dict
    def __iter__(self):
        return iter(self.dict)
    def __len__(self):
        return len(self.dict)
    def __str__(self):
        return str(self.dict)
    def __repr__(self):
        return repr(self.dict)



if __name__ == "__main__":
    def lowercase(item):
        return item.lower()
    example_data = {"SoMeTHING" : 123,
                    "randomString" : 321}

    thing_dict = NormalizedDict(lowercase, example_data)
    print(thing_dict) # The keys from example_data are now lower case!
    print(thing_dict["something"]) # 123

    for key in thing_dict:
        # Still works because the key will be set to lower case again
        # when accessing the dict.
        print(thing_dict[key.upper()])

    thing_dict.pop("SOMETHING")
    print(thing_dict)




