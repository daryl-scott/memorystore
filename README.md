# memorystore
Provides a dictionary interface to a list of lists of list of tuples.

## Installation

### From Source Code

Clone or download the source code, generate wheel file, and install the wheel file using pip.

```bash
python setup.py bdist_wheel
cd dist
python -m pip install --no-index --find-links=. memorystore
```

## Usage

```python
>>> from memorystore import MemoryStore

# The id_property can be a one or more integers or attribute names.
>>> data = [(1, 10), (2, 20), (3, 30), (4, 40)]
>>> store = MemoryStore(data, 0)

>>> store[1]
(1, 10)

# The get_identity method returns a key for an item.
>>> item = (5, 50)
>>> store[store.get_identity(item)] = item
>>> store[5]
(5, 50)

# The query method returns items that meet specific criteria.
>>> predicate = lambda item: item[1] >= 30
>>> store.query(predicate)
[(3, 30), (4, 40), (5, 50)]
```

## Running the tests

```python
python -m unittest tests.test_memorystore.MemoryStoreTestCase
```

## License
[MIT](https://choosealicense.com/licenses/mit/)