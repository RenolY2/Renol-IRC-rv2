import yaml

from collections import MutableMapping

from misc.yaml_additions import Ordered_Loader, Ordered_Dumper

# Through the Config class, it should be possible to define
# a basic schema for validating a config file that should be
# loaded. The schema should also double as a default configuration.
class ConfigSchema(object):
    def __init__(self, schema = {}):
        self._schema = schema

    # While loading the file, we do basic verification:
    # 1) Does the loaded file contain all the keys from the schema file?
    # 2) Are the values from the loaded file the same type as in the schema file?
    # At this point, only a shallow verification can be done, which means that
    # the content of lists or dictionaries will not be verified against the schema.
    def load_file(self, fp):
        data = yaml.load(fp, Loader=Ordered_Loader)
        self.verify_data(data)

        # If this point is reached, that means no
        # exceptions were raised.
        return data

    def verify_data(self, data, schema = None, parent = ""):
        print(parent)
        if schema is None:
            schema = self._schema

        for key, schema_val in schema.items():
            # Raise an exception if the key from the schema
            # does not exist in the current config file.
            if key not in data:
                raise RuntimeError("Missing Key: {0}, default "
                                   "value: '{1}' (Type: {2})".format(parent+key,
                                                                     schema_val,
                                                                     type(schema_val)))

            current_val = data[key]

            # Raise an exception if the type of the value
            # does not match the type in the schema.
            if not isinstance(current_val, type(schema_val)):
                raise RuntimeError("Type mismatch in key '{1}{0}', is {1}, "
                                   "should be {2}".format(parent+key,
                                                          type(current_val),
                                                          type(schema_val)))

            # We recursively validate dictionary values in the config file.
            # To have meaningful key names when an exception is raised,
            # we keep track of the parent keys.
            if isinstance(schema_val, MutableMapping):
                self.verify_data(current_val, schema=schema_val, parent=key+"/")

        return True

    def save_default(self, fp):
        # We
        yaml.dump(self._schema, fp,
                  Dumper=Ordered_Dumper,
                  default_flow_style=False,
                  indent=4)




if __name__ == "__main__":
    from misc.config_templates import default_bot_config
    schema = ConfigSchema(default_bot_config)
    print(default_bot_config)

    with open("config.yaml", "w") as f:
        schema.save_default(f)
        #schema.load_file(f)
    schema = ConfigSchema({})
    with open("config_temp.yaml", "r") as f:
        result = schema.load_file(f)

    print(result)
    print(type(result))
    print(default_bot_config == result)