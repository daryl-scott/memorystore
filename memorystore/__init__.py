"""Provides a dictionary interface to a list of lists of list of tuples."""
from __future__ import absolute_import, division, print_function
from collections import OrderedDict
from operator import attrgetter, itemgetter
from six import string_types

__version__ = "2.0"

def _make_getter(id_property):
    """Return function that can fetch attr or item from its operand.

    Args:
        id_property: int, str, or sequence of int or str

    Returns:
        function: function that can fetch attr or item from its operand
    """
    all_str = lambda items: all((isinstance(item, string_types) for item in items))
    all_int = lambda items: all((isinstance(item, int) for item in items))

    if isinstance(id_property, string_types):
        result = attrgetter(id_property)
    elif isinstance(id_property, (tuple, list)) and all_str(id_property):
        result = attrgetter(*id_property)
    elif isinstance(id_property, int):
        result = itemgetter(id_property)
    elif isinstance(id_property, (tuple, list)) and all_int(id_property):
        result = itemgetter(*id_property)
    else:
        raise TypeError("Expected str, int, sequence of str or int; got %s" % id_property)

    return result

def _query(data, predicate=None, key=None, reverse=False):
    """Query data and return results as a list of items.

    Args:
        data: list of lists or list of tuples
        predicate: custom function for filtering results.
        key: custom comparison key function for sorting results.
            Set to get_identity method to sort on identity.
        reverse: If set to True, then the list elements are sorted
            as if each comparison were reversed.

    Returns:
        list: list of items
    """
    if predicate:
        result = list(filter(predicate, data))
    else:
        result = data[:]

    if key or reverse:
        result = sorted(result, key=key, reverse=reverse)

    return result

class DuplicateKeyError(Exception):
    """Raised when a duplicate key is found"""
    def __init__(self, key):
        super(DuplicateKeyError, self).__init__()
        self.key = key

    def __str__(self):
        return 'duplicate key: %r' % self.key

class MemoryStore(OrderedDict):
    """Provides a dictionary interface to a list of lists of list of tuples.

    If data is a list of tuples that support attribute access, id_property can
    be str or sequence of str values.

    If the specified key is not unique and strict=False (default),
    the first value wins.

    If the specified key is not unique and strict=True, will raise
    DuplicateKeyError.

    Attributes:
        data: list of lists or list of tuples
        id_property: int, str, or sequence of int or str
        strict: If True and key is not unique, raises DuplicateKeyError
    """
    def __init__(self, data, id_property, strict=False):
        self._id_property = id_property
        self._getter = _make_getter(id_property)
        self._strict = strict

        # Load data into dict
        super(MemoryStore, self).__init__()

        for item in data:
            key = self._getter(item)

            if strict and key in self:
                raise DuplicateKeyError(key)

            if key not in self:
                self[key] = item

    @property
    def id_property(self):
        """identity property"""
        return self._id_property

    @property
    def strict(self):
        """strict property"""
        return self._strict

    @property
    def data(self):
        """Return values as a list"""
        return list(self.values())

    def get_identity(self, item):
        """Return an object's identity as tuple or scalar value"""
        return self._getter(item)

    def query(self, predicate=None, key=None, reverse=False):
        """Query store and return results as a list of items

        Args:
            predicate: custom function for filtering results.
            key: custom comparison key function for sorting results.
                Set to get_identity method to sort on identity.
            reverse: If set to True, then the list elements are sorted
                as if each comparison were reversed.

        Returns:
            tuple: list of items
        """
        return _query(self.data, predicate, key, reverse)
