from nose.tools import assert_equal, assert_is_instance, assert_not_equal, assert_raises

from uri import URI


uri_string = 'scheme://user:pass@localhost:8000/path'


def test_uri_only_argument():
	"""Tests that the URI is parsed when passed as only argument"""
	uri = URI(uri_string)

	assert_equal(uri.uri, uri_string)


def test_uri_construction_from_components():
	"""Tests that URIs can be initialized by passing each piece individually"""

	uri = URI(host='localhost')

	assert_equal(str(uri), 'localhost')

	uri = URI(
		scheme='http',
		username='user',
		password='pass',
		host='localhost',
		port=8000,
		query='query=value',
		fragment='/fragment/path'
	)

	assert_equal(str(uri), 'http://user:pass@localhost:8000?query=value#/fragment/path')


def test_uri_invalid_initialization():
	"""Tests exception is raised when initializing URIs with invalid arguments"""

	with assert_raises(ValueError):
		URI('scheme://host/path', host='other-host')

	with assert_raises(ValueError):
		URI()

	with assert_raises(ValueError):
		URI('pi07gg34f1[\[]\`')


def test_uri_no_host_value():
	"""Tests that exception is raised when attempting to set host to None"""
	uri = URI(uri_string)

	with assert_raises(ValueError):
		uri.host = None


def test_uri_str():
	"""Test that str(URI) returns the constructed URI"""

	uri = URI(uri_string)

	assert_equal(str(uri), uri_string)
	assert_equal(str(uri), uri.uri)


def test_uri_repr():
	"""Test that a URI could be reconstructed from its repr()"""

	uri = URI(uri_string)

	assert_equal(uri, eval(repr(uri)))


def test_uri_equality():
	"""Test that two URIs are equal if all parts are equal"""

	uri1 = URI(uri_string)
	uri2 = URI(uri_string)

	assert_equal(uri1, uri2)

	uri1.port = 8901

	assert_not_equal(uri1.port, uri2.port)
	assert_not_equal(uri1, uri2)


def test_uri_port_int_cast():
	"""Test that the port value is always cast to an int"""

	uri = URI(host='localhost', port='80')

	assert_is_instance(uri.port, int)
	assert_equal(uri.port, 80)
	assert_equal(str(uri), 'localhost:80')

	uri.port = '81'
	assert_is_instance(uri.port, int)
	assert_equal(uri.port, 81)
	assert_equal(str(uri), 'localhost:81')

	uri.port = 82.0
	assert_is_instance(uri.port, int)
	assert_equal(uri.port, 82)
	assert_equal(str(uri), 'localhost:82')


def test_uri_port_range():
	"""Verify ports are within the 0-65536 range"""
	with assert_raises(ValueError):
		URI(host='localhost', port=-1)

	with assert_raises(ValueError):
		URI(host='localhost', port=65537)


def test_uri_string_validation():
	"""Basic validation that values are string types"""

	with assert_raises(ValueError):
		URI(host=1234)


def test_uri_query_dict():
	"""Test output of query_dict() method matches output of parse_qs() builtin function"""
	uri = URI('http://localhost:80/path/to/file?repeat=value1&repeat=value2&escape=escaped%20value#/fragment/path')

	assert_equal(uri.query_dict(), {
		'repeat': ['value1', 'value2'],
		'escape': ['escaped value']
	})
