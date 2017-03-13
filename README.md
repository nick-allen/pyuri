# PyURI

[![Build Status](https://travis-ci.org/nick-allen/pyuri.svg?branch=master)](https://travis-ci.org/nick-allen/pyuri)
[![Coverage Status](https://coveralls.io/repos/github/nick-allen/pyuri/badge.svg?branch=master)](https://coveralls.io/github/nick-allen/pyuri?branch=master)
[![PyPI version](https://badge.fury.io/py/pyuri.svg)](https://badge.fury.io/py/pyuri)

Better URI handling

Tested with Python 2.7 and 3.6

---

## Install

`pip install pyuri`

## Usage

Raw URI string parsing:

```python
from uri import URI

uri = URI('http://localhost:80/path/to/file?query=value#/fragment/path')

assert uri.scheme == 'http'
assert uri.host == 'localhost'
assert uri.port == 80
assert uri.path == '/path/to/file'
assert uri.query == 'query=value'
assert uri.fragment == '/fragment/path'
```

Composition by parts

```python
from uri import URI

uri = URI(scheme='ftp', host='localhost', port=8000, query='key=value')

assert str(uri) == 'ftp://localhost:8000?key=value'
```

Modification and comparison

```python
from uri import URI

uri1 = URI('https://example.com:80')
uri2 = URI('https://example.com:443/new/path')

assert uri1 != uri2

uri1.port = 443
uri1.path = '/new/path'

assert str(uri1) == 'https://example.com:443/new/path'

assert uri1 == uri2
```

Additional helpers

```python
from uri import URI

uri = URI('http://localhost:80/path/to/file?repeat=value1&repeat=value2&escape=escaped%20value#/fragment/path')

# Access query parameters as dictionary
assert uri.query_dict() == {
	'repeat': ['value1', 'value2'],
	'escape': ['escaped value']
}
```

