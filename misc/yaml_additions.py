import collections
from collections import OrderedDict

from yaml import Loader,Dumper, MappingNode
from yaml.constructor import ConstructorError

# The Ordered_Dumper and Ordered_Loader classes
# use the OrderedDict for representing and constructing
# the mapping type.
# This allows the key order to be 

class Ordered_Dumper(Dumper):
    def __init__(self, *args, **kwargs):
        super(Ordered_Dumper, self).__init__(*args, **kwargs)

        self._DictCls = OrderedDict
        self.add_representer(self._DictCls, self.represent_ordered_dict)

    # Forcing flow_style to True makes so that lists will always be
    # represented using the flow style, i.e. explicitly using brackets
    # and commas instead of using indentation.
    def represent_sequence(self, tag, sequence, flow_style=None):
        return super(Ordered_Dumper, self).represent_sequence(tag, sequence, flow_style=True)


    def represent_ordered_dict(self, tag, data, flow_style=None):
        return super(Ordered_Dumper, self).represent_dict(data.items())


class Ordered_Loader(Loader):
    _DictCls = OrderedDict

    def __init__(self, *args, **kwargs):
        super(Ordered_Loader, self).__init__(*args, **kwargs)

        self.add_constructor('tag:yaml.org,2002:map', Ordered_Loader.construct_yaml_map)

    # The following code has been taken from the yaml.constructor module to
    # replace appearances of {} with the DictCls variable.
    def construct_mapping(self, node, deep=False):
        if not isinstance(node, MappingNode):
            raise ConstructorError(None, None,
                                   "expected a mapping node, but found %s" % node.id,
                                   node.start_mark)
        mapping = self._DictCls()
        for key_node, value_node in node.value:
            key = self.construct_object(key_node, deep=deep)
            if not isinstance(key, collections.Hashable):
                raise ConstructorError("while constructing a mapping", node.start_mark,
                                       "found unhashable key", key_node.start_mark)
            value = self.construct_object(value_node, deep=deep)
            mapping[key] = value
        return mapping

    def construct_yaml_map(self, node):
        data = self._DictCls()
        yield data
        value = self.construct_mapping(node)
        data.update(value)