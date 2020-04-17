"""Test Case for the MemoryStore class"""
from __future__ import absolute_import
import unittest
from collections import namedtuple
from memorystore import MemoryStore, DuplicateKeyError

Row = namedtuple("Row", ("id", "value"))

DATA = [Row(1, 10), Row(2, 20), Row(3, 30), Row(4, 40)]

class MemoryStoreTestCase(unittest.TestCase):
    """Test Case for the MemoryStore class"""
    def test_itemgetter(self):
        """Test MemoryStore using position for the id_property"""
        store = MemoryStore(DATA, 0)
        self.assertEqual(store.get(1), DATA[0])

    def test_attrgetter(self):
        """Test MemoryStore using attribute name for the id_property"""
        store = MemoryStore(DATA, "id")
        self.assertEqual(store.get(1), DATA[0])

    def test_id_property(self):
        """Test the id_property property"""
        store = MemoryStore(DATA, 0)
        self.assertEqual(store.id_property, 0)

    def test_data(self):
        """Test the data property"""
        store = MemoryStore(DATA, 0)
        self.assertEqual(store.data, DATA)

    def test_get_identity(self):
        """Test the get_identity method"""
        store = MemoryStore(DATA, 0)
        row = Row(5, 50)
        self.assertEqual(store.get_identity(row), 5)

    def test_query(self):
        """Test the query method"""
        store = MemoryStore(DATA, "id")

        # Test predicate
        predicate = lambda item: item.value >= 30
        self.assertEqual(store.query(predicate), DATA[-2:])

        # Test key and reversed
        key = store.get_identity
        expected = list(reversed(DATA))
        self.assertEqual(store.query(key=key, reverse=True), expected)

    def test_strict(self):
        """Test strict mode"""
        data = DATA[:]
        data.append(Row(4, 50))
        self.assertRaises(DuplicateKeyError, MemoryStore, data, 0, True)

if __name__ == '__main__':
    unittest.main()
