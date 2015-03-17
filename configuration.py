import yaml


# Through the Config class, it should be possible to define
# a basic schema for validating a config file that should be
# loaded. The schema should also double as a default configuration.
class Config(object):
    def __init__(self, schema = {}):
        self._schema = schema

    # While loading the file, we do basic verification:
    # 1) Does the loaded file contain all the keys from the schema file?
    # 2) Are the values from the loaded file the same type as in the schema file?
    # At this point, only a shallow verification can be done, which means that
    # the content of lists or dictionaries will not be verified against the schema.
    def load_file(self, fp):
        data = yaml.load(fp)
        self.verify_data(data)

        # If this point is reached, that means no
        # exceptions were raised.
        return data

    def verify_data(self, data):
        for key, schema_val in self._schema.items():
            # Raise an exception if the key from the schema
            # does not exist in the current config file.
            if key not in data:
                raise RuntimeError("Missing Key: {0}, default "
                                   "value: '{1}' (Type: {2})".format(key,
                                                                     schema_val,
                                                                     type(schema_val)))

            current_val = data[key]

            # Raise an exception if the type of the value
            # does not match the type in the schema.
            if not isinstance(current_val, type(schema_val)):
                raise RuntimeError("Type mismatch in key '{0}', is {1}, "
                                   "should be {2}".format(key,
                                                          type(current_val),
                                                          type(schema_val)))
        return True

    def save_default(self, fp):
        yaml.dump(self._schema, fp)




if __name__ == "__main__":
    mySchema = {"host": "example.com",
                "port": 123213,
                "admins": ["Bla1", "bla2", "bla3"]}


    conf = Config(mySchema)

    with open("config.yaml", "w") as f:
        conf.save_default(f)


    with open("config.yaml", "r") as f:
        print(conf.load_file(f))

    # Can also be used without a schema
    schemaless_conf = Config({})
    with open("config.yaml", "r") as f:
        print(schemaless_conf.load_file(f))