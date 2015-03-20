import yaml
import os

from collections import MutableMapping, OrderedDict

from misc.yaml_additions import Ordered_Loader, Ordered_Dumper

# Through the Config class, it should be possible to define
# a basic schema for validating a config file that should be
# loaded. The schema should also double as a default configuration.


class Config(object):
    def __init__(self, filepath, schema={}):
        self._schema = schema
        self._filepath = filepath
        self.config_data = OrderedDict()

    def file_exists(self):
        if os.path.isdir(self._filepath):
            raise RuntimeError("A directory exists with file path '{0}'. "
                               "Please remove or rename it.".format(self._filepath))

        return os.path.isfile(self._filepath)

    # While loading the file, we do basic verification:
    # 1) Does the loaded file contain all the keys from the schema file?
    # 2) Are the values from the loaded file the same type as in the schema file?
    # At this point, only a shallow verification can be done, which means that
    # the content of lists or dictionaries will not be verified against the schema.
    def load_file(self, verify=True):
        with open(self._filepath, "r") as f:
            data = yaml.load(f, Loader=Ordered_Loader)

            if verify:
                self.verify_data(data)

            # If this point is reached, that means no
            # exceptions were raised.
            self.config_data = data

    def save_file(self, fp, verify=True):
        if verify:
            self.verify_data(self.config_data)

        yaml.dump(self.config_data, Dumper=Ordered_Dumper)

    def verify_data(self, data, schema=None, parent=""):
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

    def save_default(self, fp=None):
        with open(self._filepath, "w") as f:
            yaml.dump(self._schema, f,
                      Dumper=Ordered_Dumper,
                      default_flow_style=False,
                      indent=4)

    # To provide an easier way to access information from inside the
    # config data, we implement a few methods so that the Config object
    # can be used a bit like a dict.
    def __contains__(self, item):
        return item in self.config_data

    def __getitem__(self, key):
        return self.config_data[key]

    def __iter__(self):
        return iter(self.config_data)

    def __str__(self):
        return str(self.config_data)


if __name__ == "__main__":
    from misc.config_templates import default_bot_config

    MyConfig = Config("config_temp.yaml", schema=default_bot_config)

    if not MyConfig.file_exists():
        MyConfig.save_default()
        print("Created new file")

    MyConfig.load_file()

    print(MyConfig)
    print(MyConfig["User Info"])