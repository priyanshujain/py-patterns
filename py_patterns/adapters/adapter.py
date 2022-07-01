"""
This module implements adapter for one structure to another data structure
"""
from copy import copy
from py_patterns.base import BasePattern

__all__ = (
    "Adapter",
    "Field",
)


class Field(object):
    """
    This class implements field for adapting one structure to another data structure
    """

    def __init__(self, source, dtype=None, parser=None, required=True, default=None):
        """
        Initialize field
        :param source: source field
        :param type: type of field
        :param parser: parser function for the field
        :param required: is field required
        :param default: default value of field
        """
        self.source = source
        self.dtype = dtype
        self.required = required
        self.default = default
        self.parser = parser
        self.target = None

    def get_value(self, target_field, source_data):
        """
        Get value for target field
        :param target_field: target field
        :return: converted_value
        """
        self.target = target_field

        lookup_keys = []
        if not self.source:
            lookup_keys.append(target_field)
        else:
            lookup_keys = self.source.split(".")
        converted_value = self.lookup_data(lookup_keys, source_data)

        # validate data type for converted value if given
        if (
            self.dtype
            and callable(self.dtype)
            and not isinstance(converted_value, self.dtype)
        ):
            raise ValueError(
                "Field {} is of type {} but expected {}".format(
                    self.target, type(converted_value), self.dtype
                )
            )

        # parse converted value if given parser function
        if converted_value is not None:
            if self.parser and callable(self.parser):
                converted_value = self.parser(converted_value)
        return converted_value

    def lookup_data(self, lookup_keys, source_data):
        """
        Lookup data from source data
        :param lookup_keys: list of lookup keys
        :param source_data: source data
        :return: lookup_value
        """
        lookup_value = dict(source_data)
        for lookup_key in lookup_keys:
            if not isinstance(lookup_value, dict):
                if self.required:
                    raise ValueError(
                        "Field {} is required for field {} given source {}".format(
                            lookup_key, self.target, self.source
                        )
                    )
                else:
                    return self.default
            lookup_value = lookup_value.get(lookup_key, None)
        return lookup_value


class BaseAdapter(BasePattern):
    __read_methods__ = frozenset(
        [
            "get_fields",
        ]
    )


class AdapterMeta(type):
    """
    This class implements metaclass for getting declared field for adapter
    """

    def __new__(cls, name, bases, attrs):
        """
        Initialize adapter
        :param name: name of adapter
        :param bases: bases of adapter
        :param attrs: attributes of adapter
        """
        fields = {}
        for base in bases:
            if hasattr(base, "_fields"):
                fields.update(base._fields)
        for attr_name, attr_value in attrs.items():
            if isinstance(attr_value, Field):
                fields[attr_name] = attr_value
        attrs["_fields"] = fields
        return super().__new__(cls, name, bases, attrs)


class Adapter(BaseAdapter, metaclass=AdapterMeta):
    def __init__(self, source_data={}, *args, **kwargs):
        self.data = source_data
        super().__init__(*args, **kwargs)

    @property
    def fields(self):
        """
        Get fields of adapter
        :return: fields of adapter
        """
        return self.get_fields()

    def get_fields(self):
        """
        This method implements getting declared fields for adapter
        :return: declared fields
        """
        if hasattr(self, "_fields"):
            return self._fields
        return {}

    def convert(self, data=None):
        """
        This method implements converting data to adapter data structure
        :param data: data to convert
        :return: converted data
        """
        if data is None:
            data = self.data
        return self.convert_data(data)

    def convert_data(self, data):
        """
        This method implements converting data to adapter data structure
        :param data: data to convert
        :return: converted data
        """
        converted_data = {}
        for field_name, field_value in self.fields.items():
            converted_data[field_name] = field_value.get_value(field_name, data)
        return converted_data
