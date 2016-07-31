from nose.tools import assert_dict_equal, assert_is_not_none

from uri.uri import URI_REGEX


valid_uris = (
	('https://google.com/', {
		'scheme': 'https',
		'username': None,
		'password': None,
		'host': 'google.com',
		'port': None,
		'path': '/',
		'query': None,
		'fragment': None
	}),
	('postgres://user:pass@127.0.0.1:5432/db', {
		'scheme': 'postgres',
		'username': 'user',
		'password': 'pass',
		'host': '127.0.0.1',
		'port': '5432',
		'path': '/db',
		'query': None,
		'fragment': None
	}),
	('ftp://user@ftp.com?query=value', {
		'scheme': 'ftp',
		'username': 'user',
		'password': None,
		'host': 'ftp.com',
		'path': None,
		'port': None,
		'query': 'query=value',
		'fragment': None
	}),
	('localhost:8080/', {
		'scheme': None,
		'username': None,
		'password': None,
		'host': 'localhost',
		'port': '8080',
		'query': None,
		'fragment': None,
		'path': '/'
	})
)


def verify_regex_matches(uri_string, expected_match_dict):
	match = URI_REGEX.match(uri_string)
	assert_is_not_none(match)

	assert_dict_equal(
		match.groupdict(),
		expected_match_dict
	)


def test_uri_regex_matches():
	for uri_string, expected_match_dict in valid_uris:
		yield verify_regex_matches, uri_string, expected_match_dict
